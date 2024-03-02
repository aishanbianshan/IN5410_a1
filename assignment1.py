#!/usr/bin/env python3

import math
import sys
import os
from scipy.optimize import linprog
import numpy as np

# --------------------------------------- QUESTION 1
# # Constants
# peak_cost = 1  # dollars per kWh during peak hours
# non_peak_cost = 0.5  # dollars per kWh during non-peak hours
# peak_hours = range(17, 20)  # Peak hours from 5:00pm to 8:00pm

# # Power requirements for each applicant
# power_requirements = [1.94, 9.9, 1.44]

# # Objective function coefficients (cost per kWh)
# costs = [non_peak_cost if hour not in peak_hours else peak_cost for hour in range(24)]

# # Construct the constraint matrix (each row represents an applicant's power usage)
# A_eq = np.zeros((4, 24))  # 4 rows for each applicant and one for the total power usage
# for i in range(3):
#     A_eq[i, i * 8:(i + 1) * 8] = 1  # Assign 1 to the corresponding hours for each applicant
# A_eq[3, :] = 1  # Total power usage constraint

# # Define the right-hand side vector (power requirements)
# b_eq = power_requirements + [sum(power_requirements)]  # Power requirements for each applicant and total power requirement

# # Solve the linear programming problem
# result = linprog(costs, A_eq=A_eq, b_eq=b_eq)

# # Extract the optimal power usage
# optimal_usage = result.x

# # Print the optimal power usage and total cost
# print("Optimal power usage for each hour:")
# for hour, usage in enumerate(optimal_usage):
#     print(f"Hour {hour}: {usage:.2f} kWh")
# print("Total cost:", result.fun, "dollars")

# --------------------------------------------------Question 4


# Constants
peak_cost = 1  # dollars per kWh during peak hours
non_peak_cost = 0.5  # dollars per kWh during non-peak hours
peak_hours = range(17, 20)  # Peak hours from 5:00pm to 8:00pm
total_power_limit = 2  # Maximum total power usage per hour

# Power requirements and time constraints for each applicant
applicants = [
    {"power": 1.94, "hours": range(24)},  # A
    {"power": 9.9, "hours": range(24)},  # B
    {"power": 1.44, "hours": range(24)},  # C
    {"power": 2, "hours": range(10, 20)},  # D
    {"power": 9.5, "hours": range(17, 24)}  # E
]

# Objective function coefficients (cost per kWh)
costs = []
for hour in range(24):
    if hour in peak_hours:
        costs.append(peak_cost)
    else:
        costs.append(non_peak_cost)

# Construct the constraint matrix (each row represents an hour)
A_eq = np.zeros((24, 24))
for hour in range(24):
    for applicant in applicants:
        if hour in applicant["hours"]:
            A_eq[hour, hour] += 1  # Increment power usage for the corresponding hour

# Define the right-hand side vector (power requirements)
b_eq = [total_power_limit] * 24  # Total power usage limit for each hour

# Solve the linear programming problem
result = linprog(costs, A_eq=A_eq, b_eq=b_eq)

# Extract the optimal power usage
optimal_usage = result.x

# Print the optimal power usage and total cost
print("Optimal power usage for each hour:")
for hour, usage in enumerate(optimal_usage):
    print(f"Hour {hour}: {usage:.2f} kWh")
print("Total cost:", result.fun, "dollars")



