import matplotlib.pyplot as plt
import numpy as np
#import tikzplotlib

output = "figures/"

def tikzplotlib_fix_ncols(obj):
    """
    workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, which breaks tikzplotlib
    """
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)


def plot(schedule_energy_data, energy_cost):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    bar_width = 0.35
    index = np.arange(24)

    for i, (appliance, energy) in enumerate(schedule_energy_data.items()):
        ax1.bar((index - i*bar_width*0.8), energy, bar_width, label=appliance)

    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Energy consumption in kWh', color='black')
    ax1.set_title('Cost of Energy Used by Appliances')
    plt.xticks(index, [f"{i}:00" for i in range(24)], rotation=45)
    ax1.tick_params(axis='y', labelcolor='black')


    # Line plot for the cost of energy per kWh
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    energy_cost_values = list(energy_cost.values())
    ax2.plot(index, energy_cost_values, color='purple', label='Energy Cost per kWh')
    ax2.set_ylabel('Price Curve (NOK/kWh)', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')

    # Adding a legend for the line plot
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines, labels, loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_threshold(schedule_energy_data, energy_cost, max_energy):
    # plotting for question 4, threshold line
    fig, ax1 = plt.subplots(figsize=(12, 8))

    bar_width = 0.35
    index = np.arange(24)

    for i, (appliance, energy) in enumerate(schedule_energy_data.items()):
        ax1.bar((index - i*bar_width*0.8), energy, bar_width, label=appliance)

    ax1.set_xlabel('Hour of the Day')
    ax1.set_ylabel('Energy consumption in kWh', color='black')
    ax1.set_title('Cost of Energy Used by Appliances')
    plt.xticks(index, [f"{i}:00" for i in range(24)], rotation=45)
    ax1.tick_params(axis='y', labelcolor='black')


    # Line plot for the cost of energy per kWh
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    energy_cost_values = list(energy_cost.values())
    ax2.plot(index, energy_cost_values, color='purple', label='Energy Cost per kWh')
    ax2.set_ylabel('Price Curve (NOK/kWh)', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')

    adjusted_threshold_values = [max_energy[hour]*.4 for hour in range(24)]
    ax1.plot(index, adjusted_threshold_values, color='red', label='Energy Threshold')

    # Adding a legend for the line plot
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines, labels, loc='upper left')
    plt.tight_layout()
    plt.show()
