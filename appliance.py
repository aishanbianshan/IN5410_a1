

class Appliance:
    def __init__(self, shiftable, usage, duration, start=None, end=None):
        self.shiftable = shiftable
        self.usage = usage
        self.duration = duration
        self.start = start
        self.end = end
