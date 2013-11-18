from board_strip import *
from pos import *

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

    def get_occ_list(self, move_pos, board_size):
        # We only want the strip (in this direction) that goes through 'pos'
        s, s_num = self.get_strip(move_pos)
        move_ind = self.get_index(move_pos)
        min_ind = max(0, move_ind-4) # TODO: constant
        max_ind = min(move_ind+4, board_size-1)
        return s.get_occ_list(min_ind, max_ind)

    def get_captures(self, move_pos, colour):
        captures = []
        # We only want the strip (in this direction) that goes through 'pos'
        s, s_num = self.get_strip(move_pos)
        move_ind = self.get_index(move_pos)

        # Need a way to convert pos to an index and the reverse.
        indices = s.get_capture_indices(move_ind, colour)
        for cap_ind in indices:
            captures.append(self.get_pos(cap_ind, s_num))
        return captures

        #self.append_pos_for_indices(captures, indices, s_num)
        #captures.append(s.get_captures(pos, colour))


class EDirectionStrips(DirectionStrips):
    def clone(self):
        new_one = EDirectionStrips(board_size=0, clone=True)
        new_one.strips = [s.clone() for s in self.strips]
        return new_one

    def set_up_strips(self, board_size):
        for i in range(board_size+1):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        s_num = pos[1]
        return self.strips[s_num], s_num

    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[0]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        return Pos(ind, s_num)

    def get_occ(self, pos):
        return self.get_strip(pos)[0].get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos)[0].set_occ(pos[0], occ)

    def append_pos_for_indices(self, pos_list, indices, strip_num):
        for i in indices:
            p = Pos(i, strip_num)
            pos_list.append(p)

class SWDirectionStrips(DirectionStrips):
    def clone(self):
        new_one = SWDirectionStrips(self.board_size, clone=True)
        new_one.strips = [s.clone() for s in self.strips]
        new_one.board_size = self.board_size
        return new_one

    def set_up_strips(self, board_size):
        self.board_size = board_size
        for i in range(board_size*2):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        x = pos[0]
        y = pos[1]
        size = self.board_size
        s_num = size + x - y - 1
        return self.strips[s_num], s_num

    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[0]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        # s_num = size + x - y - 1, so:
        # y = size + x - s_num - 1
        y = self.board_size + ind - s_num - 1
        return Pos(ind, y)

    def get_occ(self, pos):
        return self.get_strip(pos)[0].get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos)[0].set_occ(pos[0], occ)

class SDirectionStrips(DirectionStrips):
    def clone(self):
        new_one = SDirectionStrips(board_size=0, clone=True)
        new_one.strips = [s.clone() for s in self.strips]
        return new_one

    def set_up_strips(self, board_size):
        for i in range(board_size+1):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        s_num = pos[0]
        return self.strips[s_num], s_num

    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[1]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        return Pos(s_num, ind)

    def get_occ(self, pos):
        return self.get_strip(pos)[0].get_occ(pos[1])

    def set_occ(self, pos, occ):
        self.get_strip(pos)[0].set_occ(pos[1], occ)

class SEDirectionStrips(DirectionStrips):
    def clone(self):
        new_one = SEDirectionStrips(board_size=0, clone=True)
        new_one.strips = [s.clone() for s in self.strips]
        return new_one

    def set_up_strips(self, board_size):
        for i in range(board_size*2+1):
            self.strips.append(BoardStrip())

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        x = pos[0]
        y = pos[1]
        s_num = x + y
        return self.strips[s_num], s_num

    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[0]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        return Pos(ind, s_num-ind)

    def get_occ(self, pos):
        return self.get_strip(pos)[0].get_occ(pos[0])

    def set_occ(self, pos, occ):
        self.get_strip(pos)[0].set_occ(pos[0], occ)
