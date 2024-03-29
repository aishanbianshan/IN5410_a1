import pulp
from energy import *
from plotting import *

peak_hours = range(17, 20)
peak_cost = 1
normal_cost = 0.5

random.seed(6)

energy_cost = time_of_use(peak_hours, peak_cost, normal_cost)

shiftable_appliances = {
    # EV can be charged before and after work, and can also be divided among the hours, we assume it takes 4 hours to charge
    "EV": {"energy": 2.475, "total_energy": 9.9, "hours": list(range(0, 6)) + list(range(17, 24))},
    # Dishwasher and laundry machine can only be used when noise is tolerated
    "Dishwasher": {"energy": 1.44, "hours": range(7,22)},
    "Laundry machine": {"energy": 1.94, "hours": range(7,22)},
}
# We want to limit that amount of appliances running, in this case max 2 at a time
max_simultaneous_appliances = 2

# model
model = pulp.LpProblem("ApplianceScheduling", pulp.LpMinimize)

# Define decision variables as continuous to allow partial operation
x = pulp.LpVariable.dicts("Schedule",
                          ((appliance, hour) for appliance in shiftable_appliances for hour in range(24)),
                          lowBound=0, upBound=1,
                          cat='Continuous')

# Constraint: Ensure all shiftable appliances run during their operational times
for appliance, details in shiftable_appliances.items():
    # For EV, ensure the total energy requirement is met over the charging window
    if appliance == "EV":
        model += pulp.lpSum(x[(appliance, hour)] * details["energy"] for hour in details["hours"]) >= details["total_energy"]
    else:  # Ensure other appliances run at least once
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
            schedule_energy_data[appliance][hour] = shiftable_appliances[appliance]["energy"]
            total_energy += schedule_energy_data[appliance][hour] * energy_cost[hour]

# Should be 6.64 (total energy needed * lowest price (0.5))
print(total_energy)


plot(schedule_energy_data, energy_cost)

