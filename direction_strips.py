from board_strip import *

class DirectionStrips():
    """ A list of BoardStrips for those going in a particular direction.
        The directions are E, SE, S, SW.
        For E and S there are the same number of strips as the board size.
        For SE and SW there (2*board size) - 1
    """ 

    def __init__(self, board_size, clone=False):
        self.strips = []
        if not clone:
            self.set_up_strips(board_size)

class EDirectionStrips(DirectionStrips):
    def set_up_strips(self, board_size):
        for i in range(board_size):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        return self.strips[pos[1]]

    def get_occ(self, pos):
        return self.get_strip(pos).get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos).set_occ(pos[0], occ)

class SEDirectionStrips(DirectionStrips):
    def set_up_strips(self, board_size):
        self.board_size = board_size
        for i in range(board_size*2):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        x = pos[0]
        y = pos[1]
        size = self.board_size
        return self.strips[size + x - y - 1]

    def get_occ(self, pos):
        return self.get_strip(pos).get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos).set_occ(pos[0], occ)

class SDirectionStrips(DirectionStrips):
    def set_up_strips(self, board_size):
        for i in range(board_size):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        return self.strips[pos[0]]

    def get_occ(self, pos):
        return self.get_strip(pos).get_occ(pos[1])

    def set_occ(self, pos, occ):
        self.get_strip(pos).set_occ(pos[1], occ)

class SWDirectionStrips(DirectionStrips):
    def set_up_strips(self, board_size):
        for i in range(board_size*2):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        x = pos[0]
        y = pos[1]
        return self.strips[x + y]

    def get_occ(self, pos):
        return self.get_strip(pos).get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos).set_occ(pos[0], occ)
