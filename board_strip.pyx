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

def get_occ(bs, ind):
    ret = bs >> (2 * ind)
    return ret & 3

def set_occ(bs, ind, occ):
    shift = 4 ** ind
    bs &= ~(shift + shift * 2)
    bs |= (occ * shift)
    return bs

def get_occ_list(bs, min_ind, max_ind):
    ol = [get_occ(bs, i) for i in range(min_ind, 1+max_ind)]
    return ol

# TODO: replace with a more efficient bitmask technique
def match_five_in_a_row(bs, move_ind, my_colour):
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

def match_capture_left(bs, ind, colour):
    if colour == BLACK:
        return match_black_capture_left(bs, ind)
    else:
        return match_white_capture_left(bs, ind)

def match_capture_right(bs, ind, colour):
    if colour == BLACK:
        return match_black_capture_right(bs, ind)
    else:
        return match_white_capture_right(bs, ind)

def match_pattern_left(bs,  ind, pattern):
    if ind < 3:
        # Cannot place to the left - off the board
        return ()
    shift = (ind-3) << 1
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind-1, ind-2)
    return ()

def match_pattern_right(bs, ind, pattern):
    shift = ind << 1
    occs = (bs >> shift) & FOUR_OCCS_MASK
    if occs == pattern:
        return (ind+1, ind+2)
    return ()

def match_black_capture_left(bs, ind):
    # BWWx
    return match_pattern_left(bs, ind, BLACK_CAPTURE_LEFT_PATTERN)

def match_white_capture_left(bs, ind):
    # WBBx
    return match_pattern_left(bs, ind, WHITE_CAPTURE_LEFT_PATTERN )

def match_black_capture_right(bs, ind):
    # xWWB
    return match_pattern_right(bs, ind, BLACK_CAPTURE_RIGHT_PATTERN)

def match_white_capture_right(bs, ind):
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

