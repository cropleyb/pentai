
EMPTY = 0
BLACK = 1
WHITE = 2

class BoardStrip():
    def __init__(self):
        #self.size = size
        self.occs = 0
        
    def get_occ(self, ind):
        ret = self.occs >> (2 * ind)
        return ret & 3

    def set_occ(self, ind, occ):
        shift = 4 ** ind
        self.occs &= ~(shift + shift * 2)
        self.occs |= (occ * shift)

    def match_capture_left(self, ind, colour):
        if colour == BLACK:
            return self.match_black_capture_left(ind)
        else:
            return self.match_white_capture_left(ind)

    def match_black_capture_left(self, ind):
        # BWWx
        if ind < 3:
            # Cannot capture to the left - off the board
            return ()
        shift = 4 ** (ind - 3)
        occs = (self.occs / shift) & (4 ** 3 - 1)
        pattern = BLACK + (4 * WHITE) + (16 * WHITE)
        if occs == pattern:
            return (ind-1, ind-2)
        return ()

    def match_white_capture_left(self, ind):
        # WBBx
        if ind < 3:
            # Cannot capture to the left - off the board
            return ()
        shift = 4 ** (ind - 3)
        occs = (self.occs / shift) & (4 ** 3 - 1)
        pattern = WHITE + (4 * BLACK) + (16 * BLACK)
        if occs == pattern:
            return (ind-1, ind-2)
        return ()

    def match_capture_right(self, ind, colour):
        if colour == BLACK:
            return self.match_black_capture_right(ind)
        else:
            return self.match_white_capture_right(ind)

    def match_black_capture_right(self, ind):
        # xWWB
        shift = 4 ** (ind + 1)
        occs = (self.occs / shift) & (4 ** 3 - 1)
        pattern = WHITE + (4 * WHITE) + (16 * BLACK)
        if occs == pattern:
            return (ind+1, ind+2)
        return ()

    def match_white_capture_right(self, ind):
        # xBBW
        shift = 4 ** (ind + 1)
        occs = (self.occs / shift) & (4 ** 3 - 1)
        pattern = BLACK + (4 * BLACK) + (16 * WHITE)
        if occs == pattern:
            return (ind+1, ind+2)
        return ()

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


