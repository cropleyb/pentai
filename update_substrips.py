import pdb

class LengthCounter():
    def __init__(self):
        self.counts = [0,0,0,0,0]

    def tup(self):
        return tuple(self.counts)

    def add(self, length):
        self.counts[length-1] += 1


# TODO give this a better home
def add_substrips(pattern, us_counter, them_counter):
    # pdb.set_trace()
    seen = [0, 0]

    i = 0
    old = []
    for occ in pattern:
        if occ > 0:
            seen[occ-1] +=  1
        old.append(occ)
        i += 1
        if i >= 5:
            if seen[0] > 0 and seen[1] == 0:
                us_counter.add(seen[0])
            elif seen[1] > 0 and seen[0] == 0:
                them_counter.add(seen[1])
            old_occ = old[i-5]
            if old_occ > 0:
                seen[old_occ-1] -= 1

