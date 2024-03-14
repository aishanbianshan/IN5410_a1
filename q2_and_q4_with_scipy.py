#!/usr/bin/env python3

import math
import sys
import os
from scipy.optimize import linprog
import numpy as np
import random as random

# RTP=np.array([0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43])
# RTP=[0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43]
# print("RTP=",RTP)
# print("length of RTP= ", len(RTP))
# Objective function coefficients, because we have 4 shiftable appliances, [C_i,C_i,C_i,C_i]
# the coefficient vector is a 96*1 vector for all variables in x, 
# x is a 96*1 decision vector for all A_i, B_i,C_i,D_i
c = [0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43, 
	 0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43,
	 0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43,
	 0.68, 0.68, 0.65, 0.63,0.60, 0.67,0.65,0.68,0.64, 0.68,0.63, 0.68,0.67,0.64,0.65,0.67, 0.62,1.28, 1.4, 1.13, 0.58,0.57, 0.58,0.43]
	          
# print("c=",c) 

# -------------------------------- Coefficient matrix of the equality constraints -----------------------------------------
# Initialize an empty list to store the A_eq
A_eq = []
# Create the A_eq using list comprehension
for i in range(4):
    # print("i=", i)
    row = [1 if i * 24 <= j < i * 24 + 24 else 0 for j in range(96)]
    # print(row)
    A_eq.append(row)

# Print the A_eq
# for row in A_eq:
#     print(row)

# Right-hand side of the equality constraints
b_eq = [1.44,1.94,2.5,9.9]  # Right-hand side of equality constraints

# --------------------------------- Coefficient matrix of the inequality constraints ----------------------------------------
# Create the A_ub using rows in the identity matrix for patterns
A_ub = []  
identity_matrix = np.eye(24)
for i in range (24):
	row = np.tile(identity_matrix[i], 4)
	A_ub.append(row.tolist())

# Right-hand side of the inequality constraints
hour_power_cap_vector = np.full(24, 7)# in kwh
k= np.array([ 0.77 for i in range(24)])# hourly power usage for all non-shiftable appliances
# print ("k=",k)

b_ub = hour_power_cap_vector -k  # Right-hand side of inequality constraints: 4, 1
# print(b_ub)
# Bounds for each decision variable
bounds = [(0, None) for _ in range(96)] # Non-negative bounds for A_0..A_23, B_0...B_23, C_0..C_23, D_0...D_23 all 96 variables


# # Solve the linear programming problem
# result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')  #results for Q2
result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
decision_variable_dimension = len(result.x)
print("the decision vector has the dimention of =",decision_variable_dimension)
# Check if the optimization was successful
if result.success:
    optimal_solution = result.x
    optimal_value = result.fun
    print("Optimal Solution:", optimal_solution)
    print("Optimal Value of Objective Function:", optimal_value)
else:
    print("Optimization failed. Message:", result.message)

