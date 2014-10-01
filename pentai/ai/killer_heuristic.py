
class KillerHeuristicStats(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.killers = [None] * 20

    def report_short_circuit(self, move, depth):
        self.killers[depth] = move

    def get_weighting(self, move, depth):
        try:
            if self.killers[depth] == move:
                return 10
        except KeyError:
            pass
        return 1

    def get_move(self, depth):
        try:
            return self.killers[depth]
        except KeyError:
            pass

