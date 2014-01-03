cimport cython

from defines import *

'''
cdef:
    long FOUR_OCCS_MASK
    long BLACK_CAPTURE_LEFT_PATTERN
    long WHITE_CAPTURE_LEFT_PATTERN
    long BLACK_CAPTURE_RIGHT_PATTERN
    long WHITE_CAPTURE_RIGHT_PATTERN
    long BLACK_THREAT_LEFT_PATTERN
    long WHITE_THREAT_LEFT_PATTERN
    long BLACK_THREAT_RIGHT_PATTERN
    long WHITE_THREAT_RIGHT_PATTERN
'''


# We separate out numbers representing groups of 4 occupancies
cdef long FOUR_OCCS_MASK = (4 ** 4 - 1)

# These patterns are matched against to detect captures

# BWWx
cdef long BLACK_CAPTURE_LEFT_PATTERN = BLACK + (4 * WHITE) + (16 * WHITE) # + 64 * 0
# WBBx
cdef long WHITE_CAPTURE_LEFT_PATTERN = WHITE + (4 * BLACK) + (16 * BLACK) # + 64 * 0
# xWWB
cdef long BLACK_CAPTURE_RIGHT_PATTERN = (WHITE + (4 * WHITE) + (16 * BLACK)) * 4
# xBBW
cdef long WHITE_CAPTURE_RIGHT_PATTERN = (BLACK + (4 * BLACK) + (16 * WHITE)) * 4

# These patterns are matched against to detect threats

# EWWx
cdef long BLACK_THREAT_LEFT_PATTERN =         (4 * WHITE) + (16 * WHITE) # + 64 * 0
# EBBx
cdef long WHITE_THREAT_LEFT_PATTERN =       + (4 * BLACK) + (16 * BLACK) # + 64 * 0
# EWWB
cdef long BLACK_THREAT_RIGHT_PATTERN = (WHITE + (4 * WHITE) ) * 4
# EBBW
cdef long WHITE_THREAT_RIGHT_PATTERN = (BLACK + (4 * BLACK) ) * 4

cpdef long get_occ(long bs, int ind):
    ret = bs >> (ind * 2)
    return ret & 3

cpdef long set_occ(long bs, int ind, long occ):
    cdef long shift
    shift = 4 ** ind
    #shift = 1 << (ind * 2) # Type conversion issues in C
    bs &= ~(shift + (shift << 1))
    bs |= (occ * shift)
    return bs

def get_occ_list(bs, min_ind, max_ind):
    ol = [get_occ(bs, i) for i in range(min_ind, 1+max_ind)]
    return ol

# TODO: replace with a more efficient bitmask technique
cpdef int match_five_in_a_row(long bs, int move_ind, int my_colour):
    cdef int l

    l = 1
    while l < 5:
        test_ind = move_ind + l
        next_occ = get_occ(bs, test_ind)
        if next_occ != my_colour:
            break
        l += 1

    # Now see how far the line goes in the opposite direction.
    m = -1
    while m > -5:
        test_ind = move_ind + m
        if test_ind < 0:
            # Other end of a potential line is off the edge of the board
            break
        next_occ = get_occ(bs, test_ind)
        if next_occ != my_colour:
            break
        m -= 1
    total_line_length = 1 + (l-1) - (m+1)
    return total_line_length >= 5

cpdef match_capture_left(long bs, int ind, int colour):
    if colour == BLACK:
        return match_black_capture_left(bs, ind)
    else:
        return match_white_capture_left(bs, ind)

cpdef match_capture_right(long bs, int ind, int colour):
    if colour == BLACK:
        return match_black_capture_right(bs, ind)
    else:
        return match_white_capture_right(bs, ind)

@cython.profile(False)
cdef inline match_pattern_left(long bs, int ind, long pattern):
    cdef int shift
    cdef long occs

    if ind < 3:
        # Cannot place to the left - off the board
        return ()
    shift = (ind-3) << 1
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind-1, ind-2)
    return ()

@cython.profile(False)
cdef inline match_pattern_right(long bs, int ind, long pattern):
    cdef int shift
    cdef long occs

    shift = ind << 1
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind+1, ind+2)
    return ()

@cython.profile(False)
cdef match_black_capture_left(long bs, int ind):
    # BWWx
    return match_pattern_left(bs, ind, BLACK_CAPTURE_LEFT_PATTERN)

cdef match_white_capture_left(long bs, int ind):
    # WBBx
    return match_pattern_left(bs, ind, WHITE_CAPTURE_LEFT_PATTERN )

cdef match_black_capture_right(long bs, int ind):
    # xWWB
    return match_pattern_right(bs, ind, BLACK_CAPTURE_RIGHT_PATTERN)

cdef match_white_capture_right(long bs, int ind):
    # xBBW
    return match_pattern_right(bs, ind, WHITE_CAPTURE_RIGHT_PATTERN)

def get_capture_indices(bs, ind, colour):
    captures = []
    if colour == BLACK:
        captures.extend(match_black_capture_left(bs, ind))
        captures.extend(match_black_capture_right(bs, ind))
    else:
        # WHITE
        captures.extend(match_white_capture_left(bs, ind))
        captures.extend(match_white_capture_right(bs, ind))
    return captures

def match_black_threat_left(bs, ind):
    # BWWx
    return match_pattern_left(bs, ind, BLACK_THREAT_LEFT_PATTERN)

def match_white_threat_left(bs, ind):
    # WBBx
    return match_pattern_left(bs, ind, WHITE_THREAT_LEFT_PATTERN)

def match_black_threat_right(bs, ind):
    # xWWB
    return match_pattern_right(bs, ind, BLACK_THREAT_RIGHT_PATTERN)

def match_white_threat_right(bs, ind):
    # xBBW
    return match_pattern_right(bs, ind, WHITE_THREAT_RIGHT_PATTERN)

def match_threat_left(bs, ind, colour):
    if colour == BLACK:
        return match_black_threat_left(bs, ind)
    else:
        return match_white_threat_left(bs, ind)

def match_threat_right(bs, ind, colour):
    if colour == BLACK:
        return match_black_threat_right(bs, ind)
    else:
        return match_white_threat_right(bs, ind)

def get_threat_indices(bs, ind, colour):
    threats = []
    if colour == BLACK:
        threats.extend(match_black_threat_left(bs, ind))
        threats.extend(match_black_threat_right(bs, ind))
    else:
        # WHITE
        threats.extend(match_white_threat_left(bs, ind))
        threats.extend(match_white_threat_right(bs, ind))
    return threats

#######################################

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

#######################################

# TODO: this is copy and paste from above
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

