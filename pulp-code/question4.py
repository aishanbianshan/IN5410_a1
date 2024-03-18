import pulp
import numpy as np
import matplotlib.pyplot as plt

from energy import *
from plotting import *

peak_hours = range(17, 20)
peak_cost = 1
normal_cost = 0.5
fluctuation = 0.125

#energy_cost = time_of_use(peak_hours, peak_cost, normal_cost)
energy_cost = real_time_pricing(peak_hours, peak_cost, normal_cost, fluctuation)


shiftable_appliances = {
    # EV can be charged before and after work, and can also be divided among the hours, we assume it takes 4 hours to charge
    "EV": {"energy": 2.475, "total_energy": 9.9, "hours": list(range(0, 6)) + list(range(17, 24))},
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


threshold = 5
max_energy = adjust_energy_threshold(non_shiftable_appliances, threshold)



# Create the optimization model
model = pulp.LpProblem("ApplianceScheduling", pulp.LpMinimize)

# Define decision variables as continuous to allow partial operation
x = pulp.LpVariable.dicts("Schedule",
                          ((appliance, hour) for appliance in shiftable_appliances for hour in range(24)),
                          lowBound=0, upBound=1,
                          cat='Continuous')

# Constraint: Ensure all shiftable appliances run within their operational windows
for appliance, details in shiftable_appliances.items():
    # For EV, ensure the total energy requirement is met over the charging window
    if appliance == "EV":
        model += pulp.lpSum(x[(appliance, hour)] * details["energy"] for hour in details["hours"]) >= details["total_energy"]
    else:  # Ensure other appliances run at least once, adjusting if necessary for their specific requirements
        model += pulp.lpSum(x[(appliance, hour)] for hour in details["hours"]) >= 1

# Constraint: Ensure the total energy consumption does not exceed the threshold at any hour
for hour in range(24):
    model += pulp.lpSum(x[(appliance, hour)] * shiftable_appliances[appliance]["energy"]
                        for appliance in shiftable_appliances if hour in shiftable_appliances[appliance]["hours"]) <= max_energy[hour]

max_simultaneous_appliances = 1
for hour in range(24):
    model += pulp.lpSum(x[(appliance, hour)] for appliance in shiftable_appliances if hour in shiftable_appliances[appliance]["hours"]) <= max_simultaneous_appliances


# Objective Function: Minimize energy cost, considering operational costs and schedules
model += pulp.lpSum(x[(appliance, hour)] * shiftable_appliances[appliance]["energy"] * energy_cost[hour]
                    for appliance in shiftable_appliances for hour in range(24) if hour in shiftable_appliances[appliance]["hours"])

# Solve the model
status = model.solve()

# Check and print the status
print("Status:", pulp.LpStatus[status])


schedule_energy_data = {appliance: [0 for hour in range(24)] for appliance in shiftable_appliances}

for appliance in shiftable_appliances:
    for hour in range(24):
        if pulp.value(x[(appliance, hour)]) == 1:
            # Apply the energy cost for the current hour to the energy usage
            schedule_energy_data[appliance][hour] = shiftable_appliances[appliance]["energy"] * energy_cost[hour]


fig, ax1 = plt.subplots(figsize=(12, 8))

bar_width = 0.35
index = np.arange(24)

for i, (appliance, costs) in enumerate(schedule_energy_data.items()):
    ax1.bar((index - i*bar_width*0.5), costs, bar_width, label=appliance)

ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Cost of Energy Used ($)', color='blue')
ax1.set_title('Cost of Energy Used by Shiftable Appliances and Energy Cost per Hour')
plt.xticks(index, [f"{i}:00" for i in range(24)], rotation=45)
ax1.tick_params(axis='y', labelcolor='blue')



# Line plot for the cost of energy per kWh
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
energy_cost_values = list(energy_cost.values())
ax2.plot(index, energy_cost_values, color='purple', label='Energy Cost per kWh')
ax2.set_ylabel('Energy Cost per kWh ($)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

adjusted_threshold_values = [max_energy[hour]*.4 for hour in range(24)]
ax1.plot(index, adjusted_threshold_values, color='red', label='Energy Threshold')


# Adding a legend for the line plot
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines, labels, loc='upper left')

filename = "question4"
tikzplotlib_fix_ncols(plt.gcf())
tikzplotlib.save(output + filename + ".tex",
                 axis_height='\\figH',
                 axis_width='\\figW')

plt.show()