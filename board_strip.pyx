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

class BoardStrip():
    def __init__(self, initial_val=0):
        self.occs = initial_val

    def clone(self):
        bs = BoardStrip(self.occs)
        return bs
        
    def get_occ(self, ind):
        ret = self.occs >> (2 * ind)
        return ret & 3

    def set_occ(self, ind, occ):
        shift = 4 ** ind
        self.occs &= ~(shift + shift * 2)
        self.occs |= (occ * shift)

    def get_occ_list(self, min_ind, max_ind):
        ol = [self.get_occ(i) for i in range(min_ind, 1+max_ind)]
        return ol

    # TODO: replace with a more efficient bitmask technique
    def match_five_in_a_row(self, move_ind, my_colour):
        l = 1
        while l < 5:
            test_ind = move_ind + l
            next_occ = self.get_occ(test_ind)
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
            next_occ = self.get_occ(test_ind)
            if next_occ != my_colour:
                break
            m -= 1
        total_line_length = 1 + (l-1) - (m+1)
        return total_line_length >= 5

    def match_capture_left(self, ind, colour):
        if colour == BLACK:
            return self.match_black_capture_left(ind)
        else:
            return self.match_white_capture_left(ind)

    def match_capture_right(self, ind, colour):
        if colour == BLACK:
            return self.match_black_capture_right(ind)
        else:
            return self.match_white_capture_right(ind)

    def match_pattern_left(self, ind, pattern):
        if ind < 3:
            # Cannot place to the left - off the board
            return ()
        shift = (ind-3) << 1
        occs = (self.occs >> shift) & FOUR_OCCS_MASK
        if occs == pattern:
            return (ind-1, ind-2)
        return ()

    def match_pattern_right(self, ind, pattern):
        shift = ind << 1
        occs = (self.occs >> shift) & FOUR_OCCS_MASK
        if occs == pattern:
            return (ind+1, ind+2)
        return ()

    def match_black_capture_left(self, ind):
        # BWWx
        return self.match_pattern_left(ind, BLACK_CAPTURE_LEFT_PATTERN)

    def match_white_capture_left(self, ind):
        # WBBx
        return self.match_pattern_left(ind, WHITE_CAPTURE_LEFT_PATTERN )

    def match_black_capture_right(self, ind):
        # xWWB
        return self.match_pattern_right(ind, BLACK_CAPTURE_RIGHT_PATTERN)

    def match_white_capture_right(self, ind):
        # xBBW
        return self.match_pattern_right(ind, WHITE_CAPTURE_RIGHT_PATTERN)

    def get_capture_indices(self, ind, colour):
        captures = []
        if colour == BLACK:
            captures.extend(self.match_black_capture_left(ind))
            captures.extend(self.match_black_capture_right(ind))
        else:
            # WHITE
            captures.extend(self.match_white_capture_left(ind))
            captures.extend(self.match_white_capture_right(ind))
        return captures

    def match_black_threat_left(self, ind):
        # BWWx
        return self.match_pattern_left(ind, BLACK_THREAT_LEFT_PATTERN)

    def match_white_threat_left(self, ind):
        # WBBx
        return self.match_pattern_left(ind, WHITE_THREAT_LEFT_PATTERN)

    def match_black_threat_right(self, ind):
        # xWWB
        return self.match_pattern_right(ind, BLACK_THREAT_RIGHT_PATTERN)

    def match_white_threat_right(self, ind):
        # xBBW
        return self.match_pattern_right(ind, WHITE_THREAT_RIGHT_PATTERN)

    def match_threat_left(self, ind, colour):
        if colour == BLACK:
            return self.match_black_threat_left(ind)
        else:
            return self.match_white_threat_left(ind)

    def match_threat_right(self, ind, colour):
        if colour == BLACK:
            return self.match_black_threat_right(ind)
        else:
            return self.match_white_threat_right(ind)

    def get_threat_indices(self, ind, colour):
        threats = []
        if colour == BLACK:
            threats.extend(self.match_black_threat_left(ind))
            threats.extend(self.match_black_threat_right(ind))
        else:
            # WHITE
            threats.extend(self.match_white_threat_left(ind))
            threats.extend(self.match_white_threat_right(ind))
        return threats

