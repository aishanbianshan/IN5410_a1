import matplotlib.pyplot as plt

# Constants
peak_hours = range(17, 20)  # Peak hours from 5:00pm to 8:00pm

# Power requirements and time constraints for each appliance
appliances = [
    # non-shiftable loads
    {"power": 2, "hours": range(10, 21)},  # Lighting
    {"power": 9.6, "hours": range(0, 24)},  # Heating
    {"power": 1.32, "hours": range(0, 24)},  # Refrigerator
    {
        "power": 3.9,
        "hours": [8, 9, 11, 12, 17, 18],
    },  # Stove
    {"power": 0.6, "hours": range(17, 23)},  # TV
    {"power": 0.6, "hours": range(17, 23)},  # Computer
    {"power": 0.144, "hours": range(0, 24)},  # Router
    {"power": 0.84, "hours": range(0, 24)},  # Separate freezer
    {"power": 1.2, "hours": range(17, 19)},  # Microwave
    # shiftable loads
    {"power": 1.44, "hours": range(24)},  # Dishwasher
    {"power": 1.94, "hours": range(24)},  # Laundry machine
    {"power": 2.5, "hours": range(24)},  # Dryer
    {"power": 9.9, "hours": range(24)},  # EV
]

non_shiftable_appliances = appliances[:9]
shiftable_appliances = appliances[9:]


def generate_price_curve_RTP(peak_hours: list) -> list:
    """Generate a random real-time price curve for a day

    Returns:
        list of float: the price curve in NOK per kWh
    """
    import random

    # Setting the seed to make the results reproducible
    random.seed(6)

    # Generating a random price curve that is higher during peak hours
    price_curve = [
        random.uniform(1, 1.5) if i in peak_hours else random.uniform(0.6, 0.7)
        for i in range(24)
    ]

    return price_curve


def plot_price_curve(price_curve: list) -> None:
    """Plot the price curve for a day

    Args:
        price_curve: list of float, the price curve in NOK per kWh

    Returns:
        None
    """
    plt.step(range(24), price_curve, where="post")
    plt.xlabel("Hour")
    plt.xticks(range(25), [f"{i}:00" for i in range(25)], rotation=45)
    plt.ylabel("NOK per kWh")
    plt.title("Generated price curve for a day")
    plt.ylim(0)
    plt.show()


def plot_price_curve_vs_usage(
    price_curve: list, usage: list, num_households: int = 1, number_of_EVs: int = 1
) -> None:
    """Plot the price curve and the usage curve in the same graph

    Args:
        price_curve: list of float, the price curve in NOK per kWh
        usage: list of float, the usage in kWh for each hour.
        num_households: int, number of household. Default is 1
        number_of_EVs: int, number of electric vehicles. Default is 1

    Returns:
        None
    """
    price_curve = list(price_curve)
    usage = list(usage)

    # appending 0 to the end of the lists to make them the same length
    price_curve.append(price_curve[-1])
    usage.append(usage[-1])

    # plotting the optimal power usage against the price curve
    plt.step(range(25), price_curve, label="Price curve (NOK/kWh)", where="post")
    plt.step(range(25), usage, label="Optimal power usage (kWh)", where="post")
    plt.suptitle("Optimal power usage vs. price curve")
    plt.title(
        f"Number of households = {num_households}, Number of EVs = {number_of_EVs}",
        fontsize=8,
    )
    plt.xlabel("Hour")
    plt.xticks(range(25), [f"{i}:00" for i in range(25)], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def print_price_curve(price_curve: list) -> None:
    """Print the price curve in a human readable format

    Args:
        price_curve: list of float, the price curve in NOK per kWh

    Returns:
        None
    """
    print("Price curve for a day:")
    print("-" * 30)
    print(f"{'Hour':<4} {'Time of day':<13} {'NOK per kWh':>10}")
    print("-" * 30)
    for hour, price in enumerate(price_curve):
        print(f"{hour + 1:<4} ({hour:02d}.00-{hour + 1:02d}.00) {price:>10.3f}")
    print("-" * 30)


def print_optimal_usage(costs: list, usage: list):
    """Print the optimal usage in a human readable format

    Args:
        costs: list of float, the price curve in NOK per kWh
        usage: list of float, the usage in kWh for each hour. Example: [(10, 5.5)] for 5.5 kWh at 10:00am

    Returns:
        None
    """
    # Calculating the total cost of the usage
    total_cost = sum([costs[i] * usage for i, usage in enumerate(usage)])

    print("Optimal power usage for each hour:")
    print("-" * 60)
    print(
        f"{'Hour':<4} | {'Time of day':<13} | {'NOK per kWh':>15} | {'Usage (kWh)':>15}"
    )
    print("-" * 60)
    for hour, usage in enumerate(usage):
        print(
            f"{hour + 1:<4} | ({hour:02d}.00-{hour + 1:02d}.00) | {costs[hour]:>15.3f} | {usage:>15.3f}"
        )
    print("-" * 60)
    print(f"{'Total cost:':<37} {total_cost:>15.2f} NOK")
