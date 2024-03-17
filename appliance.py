

class Appliance:
    def __init__(self, power_usage, duration, start=None, end=None):
        self.shiftable = start is not None
        self.power_usage = power_usage
        self.duration = duration
        self.start = start
        self.end = end


class Household:
    def __init__(self, *appliances):
        self.appliances = appliances

