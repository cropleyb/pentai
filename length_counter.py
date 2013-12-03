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


from defines import *
from candidate_accumulator import *

"""
Detect and report indices that build on or interfere with a 
possibly fragmented line, as well as counting these possibilities
"""

def process_substrips(pattern, ca, us_counter, them_counter, inc):
    """ This complex little algorithm calculates the contributions
    of a given line of pieces ("pattern") to the totals count.
    We only count the number of ways in which a line of 5 is possible.
    ca: candidate accumulator
    """
    seen = [0, 0, 0]
     
    i = 0
    old = []
    empty_list = []
    first_empty = 0

    # Go through the occupancies of the strip of positions
    # passed to us.
    for occ in pattern:
        if occ != EMPTY:
            seen[occ] += 1 # BLACK or WHITE
        else:
            empty_list.append(i)

        # Keep track of old occupancies for undoing later
        old.append(occ)

        i += 1

        # We only start counting once we have reached a length of 5
        if i >= COUNT_LENGTH:
            try:
                while empty_list[first_empty] < i - COUNT_LENGTH:
                    first_empty += 1
            except IndexError:
                pass
            empties_to_report = tuple(empty_list[first_empty:])
            sb = seen[BLACK]
            sw = seen[WHITE]
            # Have we only seen one colour in that line of 5?
            if sb > 0 and sw == 0:
                us_counter.counts[sb-1] += inc
                ca.report_length_candidate(BLACK, sb, empties_to_report)
            elif sw > 0 and sb == 0:
                them_counter.counts[sw-1] += inc
                ca.report_length_candidate(WHITE, sw, empties_to_report)

            # Ignore the first one of that 5 now.
            old_occ = old[i-COUNT_LENGTH]
            if old_occ > 0:
                seen[old_occ] -= 1

