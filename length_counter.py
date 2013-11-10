# TODO: This will need to be increased to 6 for pente-keryo
COUNT_LENGTH=5

class LengthCounter():
    def __init__(self, arr=None):
        if arr == None:
            self.counts = [0] * COUNT_LENGTH
        else:
            self.counts = arr[:]
        self.add_mode = True

    def tup(self):
        return tuple(self.counts)

    def set_add_mode(self, m):
        self.add_mode = m

    def process(self, length):
        if self.add_mode:
            self.counts[length-1] += 1
        else:
            self.counts[length-1] -= 1

    def __eq__(self, other):
        return self.counts == other

    def __repr__(self):
        return str(self.counts)

    def __len__(self):
        return COUNT_LENGTH

    def __getitem__(self, i):
        return self.counts[i]



# TODO give this a better home
def add_substrips(pattern, us_counter, them_counter):
    process_substrips(pattern, us_counter, them_counter)

def remove_substrips(pattern, us_counter, them_counter):
    process_substrips(pattern, us_counter, them_counter)

def process_substrips(pattern, us_counter, them_counter):
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
                us_counter.process(seen[0])
            elif seen[1] > 0 and seen[0] == 0:
                them_counter.process(seen[1])
            old_occ = old[i-COUNT_LENGTH]
            if old_occ > 0:
                seen[old_occ-1] -= 1
