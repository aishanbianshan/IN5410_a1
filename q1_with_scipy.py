#!/usr/bin/env python3

import math
import sys
import os
from scipy.optimize import linprog
import numpy as np
import random as random

num_hours=24
peak_hours = range(17, 21)  # Peak hours from 5:00pm to 8:00pm
# # --------------------------------------- Q 1 solution ------------------
# Constants
peak_cost = 1  # dollars per kWh during peak hours
non_peak_cost = 0.5  # dollars per kWh during non-peak hours
peak_hours = range(17, 21)  # Peak hours from 5:00pm to 8:00pm

# Power requirements for each applicant
power_requirements = [1.94, 9.9, 1.44]

# Objective function coefficients (cost per kWh)
costs = [non_peak_cost if hour not in peak_hours else peak_cost for hour in range(24)]
print("EIWAECN costs= ",costs)

# Construct the constraint matrix (each row represents an applicant's power usage)
A_eq = np.zeros((4, 24))  # 4 rows for each applicant and one for the total power usage
for i in range(3):
	# A_eq[i,:] =1
    A_eq[i, i * 8:(i + 1) * 8] = 1  # Assign 1 to the corresponding hours for each applicant
A_eq[3, :] = 1  # Total power usage constraint
print("EIWAECN A_eq= ", A_eq)

# Define the right-hand side vector (power requirements)
b_eq = power_requirements + [sum(power_requirements)]  # Power requirements for each applicant and total power requirement
print ("EIWAECN b_eq= ",b_eq)
# Solve the linear programming problem
result = linprog(costs, A_eq=A_eq, b_eq=b_eq)

print("EIWAECN result = ",result)
# Extract the optimal power usage
optimal_usage = result.x

# Print the optimal power usage and total cost
print("Optimal power usage for each hour:")
for hour, usage in enumerate(optimal_usage):
    print(f"Hour {hour}: {usage:.2f} kWh")
print("Total cost:", result.fun, "dollars")

