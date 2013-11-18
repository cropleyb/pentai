# TODO: This will need to be increased to 6 for pente-keryo
COUNT_LENGTH=5

class LengthCounter():
    def __init__(self, arr=None):
        if arr == None:
            self.counts = [0] * COUNT_LENGTH
        else:
            self.counts = arr[:]

    def tup(self):
        return tuple(self.counts)

    def process(self, length, add):
        if add:
            self.counts[length-1] += 1
        else:
            self.counts[length-1] -= 1
        assert self.counts[length-1] >= 0

    def __eq__(self, other):
        return self.counts == other

    def __repr__(self):
        return str(self.counts)

    def __len__(self):
        return COUNT_LENGTH

    def __getitem__(self, i):
        return self.counts[i]

def process_substrips(pattern, us_counter, them_counter, add):
    """ This complex little algorithm calculates the contributions
    of a given line of pieces ("pattern") to the totals count.
    We only count the number of ways in which a line of 5 is possible. """
    seen = [0, 0]

    i = 0
    old = []
    for occ in pattern:
        if occ > 0:
            seen[occ-1] +=  1
        old.append(occ)
        i += 1
        if i >= COUNT_LENGTH:
            if seen[0] > 0 and seen[1] == 0:
                us_counter.process(seen[0],add)
            elif seen[1] > 0 and seen[0] == 0:
                them_counter.process(seen[1],add)
            old_occ = old[i-COUNT_LENGTH]
            if old_occ > 0:
                seen[old_occ-1] -= 1

