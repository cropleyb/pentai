from board_strip import *

def process_takes(bs, ind, strip_min, strip_max, us, inc):
    """
    bs is the board strip that we are looking through
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    [ind, ... ind+3] for capture left
    [ind-3, ..., ind] for capture right
    """
    for i in range(max(strip_min+3, ind), 1 + min(ind+3, strip_max)):
        if len(match_black_capture_left(bs, i)) > 0:
            us.report_take(BLACK, i, inc)
        if len(match_white_capture_left(bs, i)) > 0:
            us.report_take(WHITE, i, inc)

    for i in range(max(strip_min,ind-3), 1 + min(strip_max-3,ind)):
        if len(match_black_capture_right(bs, i)) > 0:
            us.report_take(BLACK, i, inc)
        if len(match_white_capture_right(bs, i)) > 0:
            us.report_take(WHITE, i, inc)

