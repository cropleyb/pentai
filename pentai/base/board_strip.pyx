cimport cython
# cython: profile=True

from pentai.base.defines import *

from libc.stdint cimport uint64_t as U64

'''
cdef:
    U64 FOUR_OCCS_MASK
    U64 P1_CAPTURE_LEFT_PATTERN
    U64 P2_CAPTURE_LEFT_PATTERN
    U64 P1_CAPTURE_RIGHT_PATTERN
    U64 P2_CAPTURE_RIGHT_PATTERN
    U64 P1_THREAT_LEFT_PATTERN
    U64 P2_THREAT_LEFT_PATTERN
    U64 P1_THREAT_RIGHT_PATTERN
    U64 P2_THREAT_RIGHT_PATTERN
'''

# We separate out numbers representing groups of 4 occupancies
cdef U64 FOUR_OCCS_MASK = (4 ** 4 - 1)

cdef U64 FIVE_OCCS_MASK = (4 ** 5 - 1)

cdef U64 SIX_OCCS_MASK = (4 ** 6 - 1)

# These patterns are matched against to detect captures

# BWWx
cdef U64 P1_CAPTURE_LEFT_PATTERN = P1 + (4 * P2) + (16 * P2) # + 64 * 0
# WBBx
cdef U64 P2_CAPTURE_LEFT_PATTERN = P2 + (4 * P1) + (16 * P1) # + 64 * 0
# xWWB
cdef U64 P1_CAPTURE_RIGHT_PATTERN = (P2 + (4 * P2) + (16 * P1)) * 4
# xBBW
cdef U64 P2_CAPTURE_RIGHT_PATTERN = (P1 + (4 * P1) + (16 * P2)) * 4

# These patterns are matched against to detect threats

# EWWx
cdef U64 P1_THREAT_LEFT_PATTERN =         (4 * P2) + ((4**2) * P2) # + 4**3 * 0
# EBBx
cdef U64 P2_THREAT_LEFT_PATTERN =         (4 * P1) + ((4**2) * P1) # + 4**3 * 0

# TODO: P1_THREAT_LEFT_PATTERN == P1_THREAT_RIGHT_PATTERN?!
# EWWB
cdef U64 P1_THREAT_RIGHT_PATTERN = (P2 + (4 * P2) ) * 4
# EBBW
cdef U64 P2_THREAT_RIGHT_PATTERN = (P1 + (4 * P1) ) * 4

# BBBBB
cdef U64 P1_FIVE_PATTERN = P1 + 4 * P1 + (4**2) * P1 + (4**3) * P1 + (4**4) * P1
# WWWWW
cdef U64 P2_FIVE_PATTERN = P2 + 4 * P2 + (4**2) * P2 + (4**3) * P2 + (4**4) * P2
# WBBBBW
cdef U64 P1_ENCLOSED_PATTERN = P2 + 4 * P1 + (4**2) * P1 + (4**3) * P1 + (4**4) * P1 + (4**5) * P2
# BWWWWB
cdef U64 P2_ENCLOSED_PATTERN = P1 + 4 * P2 + (4**2) * P2 + (4**3) * P2 + (4**4) * P2 + (4**5) * P1

cpdef U64 get_occ(U64 bs, U64 ind):
    ret = bs >> (ind * 2UL)
    return ret & 3UL

cpdef U64 set_occ(U64 bs, U64 ind, U64 occ):
    cdef U64 shift
    shift = 4UL ** ind
    #shift = 1 << (ind * 2) # Type conversion issues in C
    bs &= ~(shift + (shift << 1UL))
    bs |= (occ * shift)
    return bs

# This method is only used for unit testing of the setting functions, AFAIK
def get_occ_list(bs, min_ind, max_ind):
    ol = [get_occ(bs, i) for i in range(min_ind, 1+max_ind)]
    return ol


cpdef int match_five_in_a_row(U64 bs, U64 move_ind, int colour):
    if colour == P1:
        pattern = P1_FIVE_PATTERN
    else:
        pattern = P2_FIVE_PATTERN
    return match_five_inner(bs, move_ind, pattern)
    

cdef int match_five_inner(U64 bs, U64 move_ind, U64 pattern):
    cdef int l
    cdef U64 to_right
    cdef U64 occs

    l = move_ind - 4UL
    if l < 0:
        l = 0

    to_right = bs >> (l << 1UL)
    while l <= move_ind:
        occs = to_right & FIVE_OCCS_MASK
        if occs == pattern:
            return True
        to_right >>= 2UL
        l += 1UL
    return False

######################################################################

# Test code only
cpdef int match_enclosed_four(U64 bs, U64 move_ind, int colour):
    if colour == P1:
        pattern = P1_ENCLOSED_PATTERN
    else:
        pattern = P2_ENCLOSED_PATTERN

    return match_six_inner(bs, move_ind, pattern)

    
# This probably misses an extremely rare pattern of two enclosed 4s
# but I'd be astonished if this has ever occurred.
cdef int match_six_inner(U64 bs, U64 move_ind, U64 pattern):
    cdef int l
    cdef U64 to_right
    cdef U64 occs

    l = move_ind - 5UL
    if l < 0:
        l = 0

    to_right = bs >> (l << 1UL)
    while l <= move_ind:
        occs = to_right & SIX_OCCS_MASK
        if occs == pattern:
            return True
        to_right >>= 2UL
        l += 1UL
    return False

######################################################################

cpdef match_capture_left(U64 bs, U64 ind, int colour):
    if colour == P1:
        return match_black_capture_left(bs, ind)
    else:
        return match_white_capture_left(bs, ind)

cpdef match_capture_right(U64 bs, U64 ind, int colour):
    if colour == P1:
        return match_black_capture_right(bs, ind)
    else:
        return match_white_capture_right(bs, ind)

@cython.profile(False)
cdef inline match_pattern_left(U64 bs, U64 ind, U64 pattern):
    cdef U64 shift
    cdef U64 occs

    if ind < 3UL:
        # Cannot place to the left - off the board
        return ()
    shift = (ind-3UL) << 1UL
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind-1UL, ind-2UL)
    return ()

@cython.profile(False)
cdef inline match_pattern_right(U64 bs, U64 ind, U64 pattern):
    cdef U64 shift
    cdef U64 occs

    shift = ind << 1UL
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind+1UL, ind+2UL)
    return ()

@cython.profile(False)
cdef match_black_capture_left(U64 bs, U64 ind):
    # BWWx
    return match_pattern_left(bs, ind, P1_CAPTURE_LEFT_PATTERN)

cdef match_white_capture_left(U64 bs, U64 ind):
    # WBBx
    return match_pattern_left(bs, ind, P2_CAPTURE_LEFT_PATTERN )

cdef match_black_capture_right(U64 bs, U64 ind):
    # xWWB
    return match_pattern_right(bs, ind, P1_CAPTURE_RIGHT_PATTERN)

cdef match_white_capture_right(U64 bs, U64 ind):
    # xBBW
    return match_pattern_right(bs, ind, P2_CAPTURE_RIGHT_PATTERN)

def get_capture_indices(bs, ind, colour):
    captures = []
    if colour == P1:
        captures.extend(match_black_capture_left(bs, ind))
        captures.extend(match_black_capture_right(bs, ind))
    else:
        # P2
        captures.extend(match_white_capture_left(bs, ind))
        captures.extend(match_white_capture_right(bs, ind))
    return captures

def match_black_threat_left(bs, ind):
    # BWWx
    return match_pattern_left(bs, ind, P1_THREAT_LEFT_PATTERN)

def match_white_threat_left(bs, ind):
    # WBBx
    return match_pattern_left(bs, ind, P2_THREAT_LEFT_PATTERN)

def match_black_threat_right(bs, ind):
    # xWWB
    return match_pattern_right(bs, ind, P1_THREAT_RIGHT_PATTERN)

def match_white_threat_right(bs, ind):
    # xBBW
    return match_pattern_right(bs, ind, P2_THREAT_RIGHT_PATTERN)

def match_threat_left(bs, ind, colour):
    if colour == P1:
        return match_black_threat_left(bs, ind)
    else:
        return match_white_threat_left(bs, ind)

def match_threat_right(bs, ind, colour):
    if colour == P1:
        return match_black_threat_right(bs, ind)
    else:
        return match_white_threat_right(bs, ind)

#######################################

def process_takes(bs, ind, strip_min, strip_max, us, inc):
    """
    bs is the board strip that we are looking through
    ind is the index of the affected position, only the 3 positions
    to its left and 3 to the right need to be examined.
    [ind, ..., ind+3] for capture left
    [ind-3, ..., ind] for capture right
    """
    # Why is iteration required? Ah, because this is really for counting
    # potential takes.
    for i in range(max(strip_min+3, ind), 1 + min(ind+3, strip_max)):
        if len(match_black_capture_left(bs, i)) > 0:
            us.report_take(P1, i, inc)
        if len(match_white_capture_left(bs, i)) > 0:
            us.report_take(P2, i, inc)

    for i in range(max(strip_min,ind-3), 1 + min(strip_max-3,ind)):
        if len(match_black_capture_right(bs, i)) > 0:
            us.report_take(P1, i, inc)
        if len(match_white_capture_right(bs, i)) > 0:
            us.report_take(P2, i, inc)

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
            us.report_threat(P1, i, inc)
        if len(match_white_threat_left(bs, i)) > 0:
            us.report_threat(P2, i, inc)

    for i in range(max(strip_min,ind-3), 1 + min(strip_max-3,ind)):
        if len(match_black_threat_right(bs, i)) > 0:
            us.report_threat(P1, i, inc)
        if len(match_white_threat_right(bs, i)) > 0:
            us.report_threat(P2, i, inc)

#######################################

cpdef process_enclosed_fours(U64 bs, U64 move_ind, us, int inc):
    if match_six_inner(bs, move_ind, P1_ENCLOSED_PATTERN):
        us.report_enclosed_four(P1, inc)
    if match_six_inner(bs, move_ind, P2_ENCLOSED_PATTERN):
        us.report_enclosed_four(P2, inc)

