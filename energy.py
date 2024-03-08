"""
@param peak_hours - list of peak hours
@param peak_cost - the cost of energy during peak hours
@param non_peak_cost - the cost of energy during non-peak hours
returns a list of energy prices varying from peak and non-peak hours
"""
def time_of_use(peak_hours, peak_cost, non_peak_cost):
    prices = []
    for hour in range(24):
        if hour in peak_hours:
            prices.append(peak_cost)
        else:
            prices.append(non_peak_cost)
    return prices

def real_time_pricing():
    # TODO: same but with randomness
    pass



if __name__ == "__main__":
    peak_hours = range(17, 20)
    peak_cost = 1
    non_peak_cost = 0.5
    hourly_cost = time_of_use(peak_hours, peak_cost, non_peak_cost)
    print(hourly_cost)

