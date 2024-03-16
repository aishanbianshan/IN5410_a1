#!/usr/bin/env python3

import math
import sys
import os
from scipy.optimize import linprog
import numpy as np
import random as random


# -------------------------------- Solution for Q3 when all 30 households have dishwasher, laundry machine and dryer -----------------------------------------

# Objective function coefficients, because we have 3 shiftable appliances, [A_i,B_i,C_i]
# the coefficient vector is a 72*1 vector for all variables in x, 
# x is a 72*1 decision vector for all A_i, B_i,C_i
c= [0.68,0.68,0.65,0.63,0.60,0.67,0.65,0.68,0.64,0.68,0.63,0.68,0.67,0.64,0.65,0.67, 0.62,1.28,1.40,1.13,0.68,0.67,0.68, 0.63,
    0.68,0.68,0.65,0.63,0.60,0.67,0.65,0.68,0.64,0.68,0.63,0.68,0.67,0.64,0.65,0.67, 0.62,1.28,1.40,1.13,0.68,0.67,0.68, 0.63,
    0.68,0.68,0.65,0.63,0.60,0.67,0.65,0.68,0.64,0.68,0.63,0.68,0.67,0.64,0.65,0.67, 0.62,1.28,1.40,1.13,0.68,0.67,0.68, 0.63]

# -------------------------------- equality constraints -----------------------------------------
# Initialize an empty list to store the A_eq
A_eq = []
# Create the A_eq using list comprehension
for i in range(3):
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(72)]
    A_eq.append(row)

# Right-hand side of the equality constraints
b_eq = [1.44,1.94,2.5]  # Right-hand side of equality constraints

# Bounds for each decision variable
bounds = [(0, None) for _ in range(72)] # Non-negative bounds for A_0..A_23, B_0...B_23, C_0..C_23, D_0...D_23 all 96 variables


# # Solve the linear programming problem for 3 shiftable appliances for all 30 households
result_3_all = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs') 
decision_variable_dimension = len(result_3_all.x)

# Check if the optimization was successful
if result_3_all.success:
    optimal_solution_3_all = result_3_all.x
    optimal_value_3_all = result_3_all.fun
    print("Optimal Solution for Q3 when each household has dishwasher, laundry machine and dryer:", optimal_solution_3_all)
    print("Optimal Value of Objective Function(lowest cost for using the above three appliances in a day in NOK):", optimal_value_3_all)
else:
    print("Optimization failed. Message:", result_3_all.message)

print()
# -------------------------------- Solution for Q3 when a fraction of households have EV-----------------------------------------


number_of_EV = 5

# RTP as the pattern for coefficient vector
pattern = np.array([0.68,0.68,0.65,0.63,0.60,0.67,0.65,0.68,0.64,0.68,0.63,0.68,0.67,0.64,0.65,0.67, 0.62,1.28,1.40,1.13,0.68,0.67,0.68, 0.63])

# Repeat the pattern n times
coefficient_vecor = np.tile(pattern, number_of_EV)

# our aim is to minimize coefficient vector C transposed times x, x as the decision vector with dimension of n*24 by 1
# such that A_eq * x = b_eq
EV_A_eq=[]
for i in range(number_of_EV):
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(24*number_of_EV)]
    EV_A_eq.append(row)

EV_b_eq = np.tile (9.9, number_of_EV)

# # Bounds for each decision variable
EV_bounds = [(0, None) for _ in range(24*number_of_EV)] # Non-negative bounds all variables in x

# # Solve the linear programming problem for n households with EV in their back yards
result_3_ev = linprog(coefficient_vecor, A_eq=EV_A_eq, b_eq=EV_b_eq, bounds=EV_bounds, method='highs') 

# Check if the optimization was successful
if result_3_ev.success:
    optimal_solution_3_ev = result_3_ev.x
    optimal_value_3_ev = result_3_ev.fun
    print("Optimal Solution for Q3 when only {} households have EV :". format(number_of_EV), optimal_solution_3_ev)
    print("Optimal Value of Objective Function (lowest cost for charging {} EVs in the community in a day is {} NOK)". format(number_of_EV, optimal_value_3_ev))
else:
    print("Optimization failed. Message:", result_3_ev.message)


print("In total, this community, consists 30 households, with {} of them having EVs, will have the minimized power cost of {} NOK per day". 
    format(number_of_EV, optimal_value_3_all + optimal_value_3_ev))

