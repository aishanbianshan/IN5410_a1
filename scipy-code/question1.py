from utility import *
from scipy.optimize import linprog
import numpy as np

# Constants
peak_cost = 1  # dollars per kWh during peak hours
non_peak_cost = 0.5  # dollars per kWh during non-peak hours
peak_hours = range(17, 20)  # Peak hours from 5:00pm to 8:00pm

# Power requirements for each applicant (in kWh)
power_requirements = [1.94, 9.9, 1.44]  # Laundry machine  # EV charger  # Dishwasher

# Objective function coefficients (cost per kWh)
costs = [non_peak_cost if hour not in peak_hours else peak_cost for hour in range(24)]

# Coefficients for the equality constraint (power requirements)
c = np.tile(costs, len(power_requirements))

# Coefficients for the equality constraint (power requirements)
A_eq = np.kron(np.eye(len(power_requirements)), np.ones((1, 24)))

# Right-hand side for the equality constraint (power requirements)
b_eq = np.array(power_requirements)

# Solve the linear programming problem
result = linprog(c, A_eq=A_eq, b_eq=b_eq)

print(f"Optimal cost: {result.fun} for shiftable appliances")

# Extract the optimal power usage and reshape it to get the usage for each appliance at each hour
optimal_usage = result.x.reshape(-1, 24)

# sum the power usage for each hour
optimal_usage = np.sum(optimal_usage, axis=0)
print_optimal_usage(costs, optimal_usage)
