
class HistoryHeuristicStats(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.history = {}

    def report_short_circuit(self, move, depth):
        # rev_depth = self.max_depth - depth # TODO?
        try:
            self.history[move] += 2**depth
        except KeyError:
            self.history[move] = 2**depth

    def get_weighting(self, move, depth):
        try:
            return self.history[move]
        except KeyError:
            pass
        return 1

