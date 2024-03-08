import random
import matplotlib.pyplot as plt

def time_of_use(peak_hours: range, peak_cost: float, non_peak_cost: float):
    """
    @param peak_hours - list of peak hours
    @param peak_cost - the cost of energy during peak hours
    @param non_peak_cost - the cost of energy during non-peak hours
    returns a list of energy prices varying from peak and non-peak hours
    """
    return [peak_cost if hour in peak_hours else non_peak_cost for hour in range(24)]


def real_time_pricing(peak_hours: range, peak_cost: float, non_peak_cost: float, fluctuation: float):
    return [peak_cost + random.uniform(-fluctuation, fluctuation) if hour in peak_hours
            else non_peak_cost + random.uniform(-fluctuation, fluctuation)
            for hour in range(24)]


def plot_price_curve(price_curve: list):
    plt.plot(price_curve)
    plt.xlabel("Hour")
    plt.ylabel("NOK per kWh")
    plt.title("Price curve")
    plt.ylim(0)
    plt.plot(price_curve, marker="o", linestyle="-")
    plt.show()


if __name__ == "__main__":
    peak_hours = range(17, 20)
    peak_cost = 1
    non_peak_cost = 0.5
    fluctuations = 0.125
    hourly_cost_tou = time_of_use(peak_hours, peak_cost, non_peak_cost)
    print(hourly_cost_tou)
    hourly_cost_rtp = real_time_pricing(peak_hours, peak_cost, non_peak_cost, fluctuations)
    print(hourly_cost_rtp)
    plot_price_curve(hourly_cost_rtp)


