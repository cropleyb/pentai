
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
