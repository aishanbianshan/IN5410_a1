import pulp
import matplotlib.pyplot as plt
import numpy as np
import random

from energy import *



# energy_cost = {hour: 1 if 17 <= hour <= 20 else 0.5 for hour in range(24)}
energy_cost = {
    hour: 1 + random.uniform(-0.125, 0.125) if 17 <= hour <= 20 else 0.5 + random.uniform(-0.2, 0.2)
    for hour in range(24)
}

# Example data structures
shiftable_appliances = {
    "dishwasher": {"energy": 1.5, "earliest_start": 0, "latest_end": 23},
    "dryer": {"energy": 1.3, "earliest_start": 0, "latest_end": 23},
    "laundry_machine": {"energy": 2, "earliest_start": 0, "latest_end": 22},
    "EV": {"energy": 3, "earliest_start": 0, "latest_end": 23},
    "C": {"energy": 3, "earliest_start": 0, "latest_end": 23},
    "D": {"energy": 2, "earliest_start": 0, "latest_end": 23},
    "E": {"energy": 1.13, "earliest_start": 0, "latest_end": 23},
}



non_shiftable_appliances = {
    "refrigerator": {"energy": 1.32, "start_hour": 0, "end_hour": 23}
}

threshold = 5

for appliance in non_shiftable_appliances:
    threshold -= non_shiftable_appliances[appliance]["energy"] / 24

print(threshold)

max_energy_threshold = {hour: threshold for hour in range(24)}




# Create the model
model = pulp.LpProblem("Appliance Scheduling", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Schedule",
                          ((appliance, hour) for appliance in shiftable_appliances for hour in range(24)),
                          cat='Binary')  # 1 if appliance runs at hour, 0 otherwise



# Operational time window constraints for shiftable appliances
for appliance, details in shiftable_appliances.items():
    model += pulp.lpSum(x[(appliance, hour)] for hour in range(details["earliest_start"], details["latest_end"] + 1)) * details["energy"] == details["energy"]

# Ensuring non-shiftable appliances are accounted for
for appliance, details in non_shiftable_appliances.items():
    model += details["energy"]  # Assuming constant operation across the specified hours


model += pulp.lpSum(x[(appliance, hour)] * shiftable_appliances[appliance]["energy"] * energy_cost[hour]
                    for appliance in shiftable_appliances
                    for hour in range(24))

# Add constraints for maximum energy threshold per hour
for hour in range(24):
    model += pulp.lpSum(x[(appliance, hour)] * shiftable_appliances[appliance]["energy"]
                        for appliance in shiftable_appliances) <= max_energy_threshold[hour]

model.solve()


schedule_energy_data = {appliance: [0 for hour in range(24)] for appliance in shiftable_appliances}

for appliance in shiftable_appliances:
    for hour in range(24):
        if pulp.value(x[(appliance, hour)]) == 1:
            # Apply the energy cost for the current hour to the energy usage
            schedule_energy_data[appliance][hour] = shiftable_appliances[appliance]["energy"] * energy_cost[hour]


# TODO: abstract to plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

bar_width = 0.35
index = np.arange(24)

for i, (appliance, costs) in enumerate(schedule_energy_data.items()):
    ax1.bar((index + i*bar_width*0.25), costs, bar_width, label=appliance)

ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Cost of Energy Used ($)', color='blue')
ax1.set_title('Cost of Energy Used by Shiftable Appliances and Energy Cost per Hour')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(range(24))
ax1.tick_params(axis='y', labelcolor='blue')

# Line plot for the cost of energy per kWh
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
energy_cost_values = list(energy_cost.values())
ax2.plot(index, energy_cost_values, color='red', label='Energy Cost per kWh', marker='o')
ax2.set_ylabel('Energy Cost per kWh ($)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Adding a legend for the line plot
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.tight_layout()
plt.show()
