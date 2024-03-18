from utility import *
from scipy.optimize import linprog
import numpy as np

# Objective function coefficients, because we have 4 shiftable appliances, [C_i,C_i,C_i,C_i]
# the coefficient vector is a 96*1 vector for all variables in x,
# x is a 96*1 decision vector for all A_i, B_i,C_i,D_i
costs = generate_price_curve_RTP(peak_hours)
c = np.tile(costs, 4)

# -------------------------------- Coefficient matrix of the equality constraints -----------------------------------------
# Initialize an empty list to store the A_eq
A_eq = []

# Create the A_eq using list comprehension
for i in range(4):
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(96)]
    A_eq.append(row)

# Right-hand side of the equality constraints
b_eq = [1.44, 1.94, 2.5, 9.9]  # Right-hand side of equality constraints

# --------------------------------- Coefficient matrix of the inequality constraints ----------------------------------------
# Create the A_ub using rows in the identity matrix for patterns
A_ub = []
identity_matrix = np.eye(24)
for i in range(24):
    row = np.tile(identity_matrix[i], 4)
    A_ub.append(row.tolist())

# Right-hand side of the inequality constraints
hour_power_cap_vector = np.full(24, 7)  # in kwh

# hourly power usage for all non-shiftable appliances
k = np.zeros(24)
for appliance in non_shiftable_appliances:
    for hour in appliance["hours"]:
        k[hour] += appliance["power"] / len(appliance["hours"])

# Right-hand side of inequality constraints: 4, 1
b_ub = hour_power_cap_vector - k

# Bounds for each decision variable
# Non-negative bounds for A_0..A_23, B_0...B_23, C_0..C_23, D_0...D_23 all 96 variables
bounds = [(0, None) for _ in range(96)]

# Solve the linear programming problem
result = linprog(
    c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs"
)

# Check if the optimization was successful
if result.success:
    # Extract the optimal power usage and reshape it to get the usage for each appliance at each hour
    optimal_usage = result.x.reshape(-1, 24)
    # sum the power usage for each hour
    optimal_usage = np.sum(optimal_usage, axis=0)

    # add non-shiftable appliances to the optimal_usage
    for appliance in non_shiftable_appliances:
        for hour in appliance["hours"]:
            optimal_usage[hour] += appliance["power"] / len(appliance["hours"])

    # plot_price_curve_vs_usage(costs, optimal_usage)
    print_optimal_usage(costs, optimal_usage)
else:
    print("Optimization failed. Message:", result.message)
