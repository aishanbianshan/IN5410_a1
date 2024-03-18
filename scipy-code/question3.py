from utility import *
from scipy.optimize import linprog
import numpy as np

# 30 households have dishwasher, laundry machine and dryer

# Objective function coefficients, because we have 3 shiftable appliances, [A_i,B_i,C_i]
# the coefficient vector is a 72*1 vector for all variables in x,
# x is a 72*1 decision vector for all A_i, B_i,C_i
costs = generate_price_curve_RTP(peak_hours)
c = np.tile(costs, 3)

# Initialize an empty list to store the A_eq
A_eq = []

# Create the A_eq using list comprehension
for i in range(3):
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(72)]
    A_eq.append(row)

# Right-hand side of the equality constraints
b_eq = [1.44, 1.94, 2.5]  # Right-hand side of equality constraints

# Bounds for each decision variable
bounds = [
    (0, None) for _ in range(72)
]  # Non-negative bounds for A_0..A_23, B_0...B_23, C_0..C_23, all 72 variables


# Solve the linear programming problem for 3 shiftable appliances for all 30 households
result_3_all = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
decision_variable_dimension = len(result_3_all.x)

# Check if the optimization was successful
if result_3_all.success:
    optimal_solution_3_all = result_3_all.x
    optimal_value_3_all = result_3_all.fun
    print(
        "Optimal Value of Objective Function(lowest cost for using the above three appliances in a day in NOK):",
        optimal_value_3_all,
    )
else:
    print("Optimization failed. Message:", result_3_all.message)

# --------------------------------  A fraction of households have EV-----------------------------------------

number_of_EV = 5

# RTP as the pattern for coefficient vector
pattern = np.array(costs)

# Repeat the pattern n times
coefficient_vecor = np.tile(pattern, number_of_EV)

# our aim is to minimize coefficient vector C transposed times x, x as the decision vector with dimension of n*24 by 1
# such that A_eq * x = b_eq
EV_A_eq = []
for i in range(number_of_EV):
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(24 * number_of_EV)]
    EV_A_eq.append(row)

EV_b_eq = np.tile(9.9, number_of_EV)

# # Bounds for each decision variable
EV_bounds = [
    (0, None) for _ in range(24 * number_of_EV)
]  # Non-negative bounds all variables in x

# # Solve the linear programming problem for n households with EV in their back yards
result_3_ev = linprog(
    coefficient_vecor, A_eq=EV_A_eq, b_eq=EV_b_eq, bounds=EV_bounds, method="highs"
)

# Check if the optimization was successful
if result_3_ev.success:
    optimal_solution_3_ev = result_3_ev.x
    optimal_value_3_ev = result_3_ev.fun
    print(
        "Optimal Value of Objective Function (lowest cost for charging {} EVs in the community in a day is {} NOK)".format(
            number_of_EV, optimal_value_3_ev
        )
    )


else:
    print("Optimization failed. Message:", result_3_ev.message)


print(
    "In total, this community, consists 30 households, with {} of them having EVs, will have the minimized power cost of {} NOK per day".format(
        number_of_EV, optimal_value_3_all + optimal_value_3_ev
    )
)

# ---------------------------------------------------- Plotting result ----------------------------------------------
# Extract the optimal power usage and reshape it to get the usage for each appliance at each hour
optimal_usage_3_all = result_3_all.x.reshape(-1, 24)
optimal_usage_EV = result_3_ev.x.reshape(-1, 24)
# sum the power usage for each hour
optimal_usage_3_all = np.sum(optimal_usage_3_all, axis=0) * 30
optimal_usage_EV = np.sum(optimal_usage_EV, axis=0)

optimal_usage = optimal_usage_3_all + optimal_usage_EV

# add non-shiftable appliances to the optimal_usage
for appliance in non_shiftable_appliances:
    for hour in appliance["hours"]:
        optimal_usage[hour] += appliance["power"] / len(appliance["hours"]) * 30


# plot_price_curve_vs_usage(costs, optimal_usage, 30, number_of_EV)
print_optimal_usage(costs, optimal_usage)
