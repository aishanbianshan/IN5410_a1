from utility import *
from scipy.optimize import linprog
import numpy as np

# power requirements for each appliance (in kWh)
p = np.array([appliance["power"] for appliance in shiftable_appliances])

# price curve for a day
RTP_costs = np.array(generate_price_curve_RTP(peak_hours))

# Objective function coefficients (cost per kWh)
c = np.tile(RTP_costs, len(p))

# Coefficients for the equality constraint (power requirements)
A_eq = np.kron(np.eye(len(p)), np.ones((1, 24)))

# Right-hand side for the equality constraint (power requirements)
b_eq = p

# Solve the linear programming problem
result = linprog(c, A_eq=A_eq, b_eq=b_eq)

print(f"Optimal soliton for shiftable appliances")
print(f"Optimal cost: {result.fun} at lowest priced hour")

# Extract the optimal power usage and reshape it to get the usage for each appliance at each hour
optimal_usage = result.x.reshape(-1, 24)

# sum the power usage for each hour
optimal_usage = np.sum(optimal_usage, axis=0)

# add non-shiftable appliances to the optimal_usage
for appliance in non_shiftable_appliances:
    for hour in appliance["hours"]:
        optimal_usage[hour] += appliance["power"] / len(appliance["hours"])

print_optimal_usage(RTP_costs, optimal_usage)
