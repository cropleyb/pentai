from defines import *
from board_strip import *

def process_takes(bs, ind, brd_size, takes, inc):
    """
    bs is the board strip that we are looking through
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    [ind, ... ind+3] for capture left
    [ind-3, ..., ind] for capture right
    """
    for i in range(ind, min(ind+4, brd_size)):
        if len(bs.match_black_capture_left(i)) > 0:
            takes[BLACK] += inc
        if len(bs.match_white_capture_left(i)) > 0:
            takes[WHITE] += inc

    for i in range(max(0,ind-3), ind+1):
        if len(bs.match_black_capture_right(i)) > 0:
            takes[BLACK] += inc
        if len(bs.match_white_capture_right(i)) > 0:
            takes[WHITE] += inc

