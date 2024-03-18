"""We need a strategy, not just the amount of the minimal energy cost. For example,
you may need to consider some questions. Is it reasonable to use all three appliances at
the same time, e.g., 2:00am which has the low energy price? How should we distribute
the power load more reasonably in the timeline?"""
import pulp
import numpy as np
from energy import *
from plotting import *

peak_hours = range(17, 20)
peak_cost = 1
normal_cost = 0.5
fluctuation = 0.125

household_number = 30
ev_fraction = 5

energy_cost = real_time_pricing(peak_hours, peak_cost, normal_cost, fluctuation)

shiftable_appliances_ev = {
    # EV can be charged before and after work, and can also be divided among the hours, we assume it takes 4 hours to charge
    "EV": {"energy": 2.475, "total_energy": 9.9, "hours": list(range(0, 6)) + list(range(17, 24))},
    # Dishwasher and laundry machine can only be used when noise is tolerated
    "Dishwasher": {"energy": 1.44, "hours": range(7,22)},
    "Laundry machine": {"energy": 1.94, "hours": range(7,22)},
    "Dryer": {"energy": 2.5, "hours": range(7,22)},
}

shiftable_appliances = {
    # Dishwasher and laundry machine can only be used when noise is tolerated
    "Dishwasher": {"energy": 1.44, "hours": range(7,22)},
    "Laundry machine": {"energy": 1.94, "hours": range(7,22)},
    "Dryer": {"energy": 2.5, "hours": range(7,22)},
}

non_shiftable_appliances = {
    "Lighting": {"energy": 2, "hours": range(10, 20)},
    "Heating": {"energy": 9.6, "hours": range(0, 23)},
    "Refrigerator": {"energy": 1.32, "hours": range(0, 23)},
    "Stove": {"energy": 3.9, "hours": [8, 9, 11, 12, 17, 18]},
    "TV": {"energy": 0.6, "hours": range(17, 22)},
    "Computer": {"energy": 0.6, "hours": range(17, 22)},
    "Router": {"energy": 0.144, "hours": range(0, 23)},
    "Separate freezer": {"energy": 0.84, "hours": range(0, 23)},
    "Microwave": {"energy": 1.2, "hours": range(17, 18)},
}

# We want to limit that amount of appliances running, in this case two at a time
max_simultaneous_appliances = 2


# model no EV
model = pulp.LpProblem("ApplianceScheduling", pulp.LpMinimize)

# Define decision variables as continuous to allow partial operation
x = pulp.LpVariable.dicts("Schedule",
                          ((appliance, hour) for appliance in shiftable_appliances for hour in range(24)),
                          lowBound=0, upBound=1,
                          cat='Continuous')

# Constraint: Ensure all shiftable appliances run during their operational times
for appliance, details in shiftable_appliances.items():
    model += pulp.lpSum(x[(appliance, hour)] for hour in details["hours"]) >= 1

# limit number of appliances running at the same time
for hour in range(24):
    model += pulp.lpSum(x[(appliance, hour)] for appliance in shiftable_appliances if hour in shiftable_appliances[appliance]["hours"]) <= max_simultaneous_appliances


# Objective Function: Minimize energy cost, considering operational costs and schedules
model += pulp.lpSum(x[(appliance, hour)] * shiftable_appliances[appliance]["energy"] * energy_cost[hour]
                    for appliance in shiftable_appliances for hour in range(24) if hour in shiftable_appliances[appliance]["hours"])

status = model.solve()


schedule_energy_data = {appliance: [0 for hour in range(24)] for appliance in shiftable_appliances}

total_energy = 0

for appliance in shiftable_appliances:
    for hour in range(24):
        if pulp.value(x[(appliance, hour)]) == 1:
            # Apply the energy cost for the current hour to the energy usage
            schedule_energy_data[appliance][hour] = shiftable_appliances[appliance]["energy"] * energy_cost[hour]
            total_energy += schedule_energy_data[appliance][hour]


# Model with EV

model_ev = pulp.LpProblem("ApplianceScheduling", pulp.LpMinimize)

# Define decision variables as continuous to allow partial operation
x_ev = pulp.LpVariable.dicts("Schedule",
                          ((appliance, hour) for appliance in shiftable_appliances_ev for hour in range(24)),
                          lowBound=0, upBound=1,
                          cat='Continuous')

# Constraint: Ensure all shiftable appliances run during their operational times
for appliance, details in shiftable_appliances_ev.items():
    # For EV, ensure the total energy requirement is met over the charging window
    if appliance == "EV":
        model_ev += pulp.lpSum(x_ev[(appliance, hour)] * details["energy"] for hour in details["hours"]) >= details["total_energy"]
    else:  # Ensure other appliances run at least once
        model_ev += pulp.lpSum(x_ev[(appliance, hour)] for hour in details["hours"]) >= 1

# limit number of appliances running at the same time
for hour in range(24):
    model_ev += pulp.lpSum(x_ev[(appliance, hour)] for appliance in shiftable_appliances_ev if hour in shiftable_appliances_ev[appliance]["hours"]) <= max_simultaneous_appliances


# Objective Function: Minimize energy cost, considering operational costs and schedules
model_ev += pulp.lpSum(x_ev[(appliance, hour)] * shiftable_appliances_ev[appliance]["energy"] * energy_cost[hour]
                    for appliance in shiftable_appliances_ev for hour in range(24) if hour in shiftable_appliances_ev[appliance]["hours"])

status = model_ev.solve()


schedule_energy_data_ev = {appliance: [0 for hour in range(24)] for appliance in shiftable_appliances_ev}

total_energy_ev = 0

for appliance in shiftable_appliances_ev:
    for hour in range(24):
        if pulp.value(x_ev[(appliance, hour)]) == 1:
            # Apply the energy cost for the current hour to the energy usage
            schedule_energy_data_ev[appliance][hour] = shiftable_appliances_ev[appliance]["energy"] * energy_cost[hour]
            total_energy += schedule_energy_data_ev[appliance][hour]

total_energy_ev *= ev_fraction
total_energy *= (household_number - ev_fraction)

total_energy_non = sum(appliance["energy"] for appliance in non_shiftable_appliances.values())

total_sum = total_energy_ev + total_energy + (total_energy_non * 30)

print(total_sum)

## Plotting


fig, ax1 = plt.subplots(figsize=(12, 8))

bar_width = 0.35
index = np.arange(24)

for i, (appliance, costs) in enumerate(schedule_energy_data.items()):
    ax1.bar((index - i*bar_width*0.8), costs, bar_width, label=appliance)

ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Cost of Energy Used ($)', color='blue')
ax1.set_title('Cost of Energy Used by Appliances')
plt.xticks(index, [f"{i}:00" for i in range(24)], rotation=45)
ax1.tick_params(axis='y', labelcolor='blue')


# Line plot for the cost of energy per kWh
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
energy_cost_values = list(energy_cost.values())
ax2.plot(index, energy_cost_values, color='purple', label='Energy Cost per kWh')
ax2.set_ylabel('Energy Cost per kWh ($)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

# Adding a legend for the line plot
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')


plt.show()
