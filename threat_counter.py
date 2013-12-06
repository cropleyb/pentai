from defines import *
from board_strip import *

# TODO: this is copy and paste from process_takes.py
def process_threats(bs, ind, brd_size, us, inc):
    """
    bs is the board strip that we are looking through
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    [ind, ... ind+3] for threat left
    [ind-3, ..., ind] for threat right
    """
    for i in range(ind, min(ind+4, brd_size)):
        if len(bs.match_black_threat_left(i)) > 0:
            us.report_threat(BLACK, i, inc)
        if len(bs.match_white_threat_left(i)) > 0:
            us.report_threat(WHITE, i, inc)

    for i in range(max(0,ind-3), ind+1):
        if len(bs.match_black_threat_right(i)) > 0:
            us.report_threat(BLACK, i, inc)
        if len(bs.match_white_threat_right(i)) > 0:
            us.report_threat(WHITE, i, inc)

