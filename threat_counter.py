from defines import *
from board_strip import *

def add_threats(occs, ind, brd_size, threats):
    """
    occs is an integer, representing the occupancies in a line.
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    ind, ... ind+3 for capture left
    ind-3, ..., ind for capture right
    """
    bs = BoardStrip(occs)
    for i in range(ind, min(ind+4, brd_size)):
        if len(bs.match_black_capture_left(i)) > 0:
            threats[BLACK] += 1
        if len(bs.match_white_capture_left(i)) > 0:
            threats[WHITE] += 1

    for i in range(max(0,ind-3), ind+1):
        if len(bs.match_black_capture_right(i)) > 0:
            threats[BLACK] += 1
        if len(bs.match_white_capture_right(i)) > 0:
            threats[WHITE] += 1

