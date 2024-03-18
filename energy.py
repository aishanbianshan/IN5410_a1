import random

def time_of_use(peak_hours: range, peak_cost: float, non_peak_cost: float):
    return {hour: peak_cost if hour in peak_hours else non_peak_cost for hour in range(24)}

def real_time_pricing(peak_hours: range, peak_cost: float, non_peak_cost: float, fluctuation: float):
    return {
        hour: peak_cost + random.uniform(-fluctuation, fluctuation) if hour in peak_hours
        else non_peak_cost + random.uniform(-fluctuation, fluctuation)
        for hour in range(24)
    }


# Function to calculate the adjusted energy threshold for each hour
def adjust_energy_threshold(non_shiftable_appliances, threshold):
    adjusted_threshold = {hour: threshold for hour in range(24)}

    for appliance, details in non_shiftable_appliances.items():
        daily_energy = details["energy"]
        operational_hours = len(details["hours"])
        hourly_energy = daily_energy / operational_hours  # Calculate hourly energy usage

        for hour in details["hours"]:
            if isinstance(hour, range):  # If the hours are specified as a range
                for h in hour:
                    adjusted_threshold[h] -= hourly_energy
            else:
                adjusted_threshold[hour] -= hourly_energy  # Subtract the hourly energy from the threshold

    return adjusted_threshold


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    peak_hours = range(17, 20)
    peak_cost = 1
    normal_cost = 0.5
    fluctuation = 0.125

    pricing = real_time_pricing(peak_hours, peak_cost, normal_cost, fluctuation)

    # Plot the data
    hours = list(pricing.keys())
    costs = list(pricing.values())

    plt.figure(figsize=(10, 6))
    plt.plot(hours, costs, marker='o', linestyle='-', color='blue')
    plt.title('Real-Time Pricing Curve')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Cost (NOK/KWh)')
    plt.xticks(hours)
    plt.show()
