import matplotlib.pyplot as plt
import tikzplotlib

output = "figures/"

def tikzplotlib_fix_ncols(obj):
    """
    workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, which breaks tikzplotlib
    """
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)


def plot_price_curve_vs_usage(costs: list, usage: list) -> None:
    ''' Plot the price curve and the usage curve in the same graph

    Args:
        price_curve: list of float, the price curve in NOK per kWh
        usage: list of float, the usage in kWh for each hour. Example: [(10, 5.5)] for 5.5 kWh at 10:00am

    Returns:
        None
    '''
    title = ""
    # plotting the optimal power usage against the price curve
    plt.step(range(24), costs, label="Price curve (NOK/kWh)")
    plt.step(range(24), usage, label="Optimal power usage (kWh)")
    plt.xlabel("Hour")
    # xticks are the hours of the day formatted hour
    plt.xticks(range(24), [f"{i}:00" for i in range(24)], rotation=45)
    title = "Optimal power usage vs price curve"
    plt.legend()
    fig = plt.gcf()
    tikzplotlib_fix_ncols(fig)
    tikzplotlib.save(output + title + ".tex",
                     axis_height='\\figH',
                     axis_width='\\figW')
