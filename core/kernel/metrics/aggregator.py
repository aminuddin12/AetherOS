class MetricsAggregator:
    def __init__(self):
        self.counters = {}
        self.histograms = {}

    def increment(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value
