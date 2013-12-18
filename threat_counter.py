from defines import *
from board_strip import *

# TODO: this is copy and paste from process_takes.py
def process_threats(bs, ind, strip_min, strip_max, us, inc):
    """
    bs is the board strip that we are looking through
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    [ind, ... ind+3] for threat left
    [ind-3, ..., ind] for threat right
    """
    for i in range(max(strip_min+3, ind), 1 + min(ind+3, strip_max)):
        if len(match_black_threat_left(bs, i)) > 0:
            us.report_threat(BLACK, i, inc)
        if len(match_white_threat_left(bs, i)) > 0:
            us.report_threat(WHITE, i, inc)

    for i in range(max(strip_min,ind-3), 1 + min(strip_max-3,ind)):
        if len(match_black_threat_right(bs, i)) > 0:
            us.report_threat(BLACK, i, inc)
        if len(match_white_threat_right(bs, i)) > 0:
            us.report_threat(WHITE, i, inc)

