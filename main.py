import numpy as np
from scipy.optimize import linprog

from appliance import Appliance
from energy import *
from plotting import *
from household import Household


laundry_machine = Appliance(1.94, 2)
EV_charger = Appliance(9.9, 3)
dishwasher = Appliance(1.44, 1)
appliances = [laundry_machine, EV_charger, dishwasher]

peak_hours = range(17,20)


power_requirements = [appliance.power_usage for appliance in appliances]
power_sum = sum(appliance.power_usage for appliance in appliances)
cost = time_of_use(peak_hours, 1, 0.5)
# Construct the constraint matrix (each row represents an applicant's power usage)
A_eq = np.zeros((4, 24))  # 4 rows for each applicant and one for the total power usage
for i in range(3):
    A_eq[i, i * 8:(i + 1) * 8] = 1  # Assign 1 to the corresponding hours for each applicant
A_eq[3, :] = 1  # Total power usage constraint

b_eq = power_requirements + [sum(power_requirements)]

result = linprog(cost, A_eq=A_eq, b_eq=b_eq, method='highs')
optimal = result.x
print("Optimal power usage for each hour:")
for hour, usage in enumerate(optimal):
    print(f"Hour {hour}: {usage:.2f} kWh")
print("Total cost:", result.fun, "dollars")

plot_price_curve_vs_usage(cost, optimal)
