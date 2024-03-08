import matplotlib.pyplot as plt

def plot_price_curve_vs_usage(costs: list, usage: list) -> None:
    ''' Plot the price curve and the usage curve in the same graph

    Args:
        price_curve: list of float, the price curve in NOK per kWh
        usage: list of float, the usage in kWh for each hour. Example: [(10, 5.5)] for 5.5 kWh at 10:00am

    Returns:
        None
    '''

    #plotting the optimal power usage against the price curve
    plt.step(range(24), costs, label="Price curve (NOK/kWh)")
    plt.step(range(24), usage, label="Optimal power usage (kWh)")
    plt.xlabel("Hour")
    # xticks are the hours of the day formatted hour
    plt.xticks(range(24), [f"{i}:00" for i in range(24)], rotation=45)

    plt.title("Optimal power usage vs price curve")
    plt.legend()
    plt.show()