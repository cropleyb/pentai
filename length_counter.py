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

    def __eq__(self, other):
        return self.counts == other

    def __repr__(self):
        return str(self.counts)

    def __len__(self):
        return COUNT_LENGTH

    def __getitem__(self, i):
        return self.counts[i]

"""
How to detect and report indices that build on / interfere with a
fragmented line?

"""

from defines import *

def process_substrips(pattern, ca, us_counter, them_counter, inc):
    """ This complex little algorithm calculates the contributions
    of a given line of pieces ("pattern") to the totals count.
    We only count the number of ways in which a line of 5 is possible.
    ca: candidate accumulator
    """
    seen = [0, 0, 0]

    i = 0
    old = []

    # Go through the occupancies of the strip of positions
    # passed to us.
    for occ in pattern:
        if occ != EMPTY:
            seen[occ] +=  1 # BLACK or WHITE

        # Keep track of old occupancies for undoing later
        old.append(occ)

        i += 1

        # We only start counting once we have reached a length of 5
        if i >= COUNT_LENGTH:
            # Have we only seen one colour in that line of 5?
            if seen[BLACK] > 0 and seen[WHITE] == 0:
                us_counter.counts[seen[BLACK]-1] += inc
            elif seen[WHITE] > 0 and seen[BLACK] == 0:
                them_counter.counts[seen[WHITE]-1] += inc

            # Ignore the first one of that 5 now.
            old_occ = old[i-COUNT_LENGTH]
            if old_occ > 0:
                seen[old_occ] -= 1

