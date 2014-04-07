from board_strip import *
import array as a_m

class DirectionStrips(object):
    """ A list of BoardStrips for those going in a particular direction.
        The directions are E, SE, S, SW.
        For E and S there are the same number of strips as the board size.
        For SE and SW there are (2*board size) - 1
    """ 

    def __init__(self, board_size, clone=False):
        self.set_up_strips(board_size)

    # This method is only used for unit testing of the setting functions, AFAIK
    def get_occ_list(self, move_pos, board_size):
        # We only want the strip (in this direction) that goes through 'pos'
        s, s_num = self.get_strip(move_pos)
        move_ind = self.get_index(move_pos)
        strip_min, strip_max = self.get_bounds(s_num, board_size)
        min_ind = max(strip_min, move_ind-4) # TODO: constant
        max_ind = min(move_ind+4, strip_max)
        return get_occ_list(s, min_ind, max_ind)

    def get_captures(self, move_pos, colour):
        captures = []
        # We only want the strip (in this direction) that goes through 'pos'
        s, s_num = self.get_strip(move_pos)
        move_ind = self.get_index(move_pos)

        # Need a way to convert pos to an index and the reverse.
        indices = get_capture_indices(s, move_ind, colour)
        for cap_ind in indices:
            captures.append(self.get_pos(cap_ind, s_num))
        return captures

class EDirectionStrips(DirectionStrips):
    '''
    Strip numbers:        Indices in each strip:
    00000                 01234
    11111                 01234
    22222                 01234
    33333                 01234
    44444                 01234
    '''
    def clone(self):
        new_one = EDirectionStrips(board_size=0, clone=True)
        new_one.strips = self.strips.__copy__()
        return new_one

    def get_bounds(self, s_num, board_size):
        return 0, board_size-1

    def set_up_strips(self, board_size):
        self.strips = a_m.array('L', [0]*board_size)

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        s_num = pos[1]
        return self.strips[s_num], s_num
        
    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[0]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        return (ind, s_num)

    def get_occ(self, pos):
        return get_occ(self.get_strip(pos)[0], pos[0])

    def set_occ(self, pos, occ):
        bs, s_num = self.get_strip(pos)
        bs_new = set_occ(bs, pos[0], occ)
        self.strips[s_num] = bs_new

    def append_pos_for_indices(self, pos_list, indices, strip_num):
        for i in indices:
            p = (i, strip_num)
            pos_list.append(p)

class SWDirectionStrips(DirectionStrips):
    '''
    Strip numbers:        Indices in each strip:
    01234                 01234
    12345                 01234
    23456                 01234
    34567                 01234
    45678                 01234
    '''
    def clone(self):
        new_one = SWDirectionStrips(self.board_size, clone=True)
        new_one.strips = self.strips.__copy__()
        new_one.board_size = self.board_size
        return new_one

    def get_bounds(self, s_num, board_size):
        # strip 0 has min 0, max 0
        # strip 2 has min 0, max 2
        # strip 4 has min 0, max 4
        # strip 6 has min 2, max 4
        # strip 8 has min 4, max 4
        if s_num < board_size:
            return 0, s_num
        else:
            return s_num-board_size+1, board_size-1

    def set_up_strips(self, board_size):
        self.board_size = board_size
        self.strips = a_m.array('L', [0]*(board_size*2))

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
        return (ind, y)

    def get_occ(self, pos):
        return get_occ(self.get_strip(pos)[0], pos[0])

    def set_occ(self, pos, occ):
        bs, s_num = self.get_strip(pos)
        bs_new = set_occ(bs, pos[0], occ)
        self.strips[s_num] = bs_new

class SDirectionStrips(DirectionStrips):
    '''
    Strip numbers:        Indices in each strip:
    01234                 00000
    01234                 11111
    01234                 22222
    01234                 33333
    01234                 44444
    '''
    def clone(self):
        new_one = SDirectionStrips(board_size=0, clone=True)
        new_one.strips = self.strips.__copy__()
        return new_one

    def get_bounds(self, s_num, board_size):
        return 0, board_size-1

    def set_up_strips(self, board_size):
        self.strips = a_m.array('L', [0]*board_size)

    def get_strip(self, pos):
        """ Get the strip that runs through pos """
        s_num = pos[0]
        return self.strips[s_num], s_num
    
    def get_bounds(self, s_num, board_size):
        return 0, board_size-1

    def get_index(self, pos):
        """ Get the index of pos in the strip returned by get_strip """
        return pos[1]

    def get_pos(self, ind, s_num):
        """ Get the position for a given index of a given strip number """
        return (s_num, ind)

    def get_occ(self, pos):
        return get_occ(self.get_strip(pos)[0], pos[1])

    def set_occ(self, pos, occ):
        bs, s_num = self.get_strip(pos)
        bs_new = set_occ(bs, pos[1], occ)
        self.strips[s_num] = bs_new

class SEDirectionStrips(DirectionStrips):
    '''
    Strip numbers:        Indices in each strip:
    45678                 01234
    34567                 01234
    23456                 01234
    12345                 01234
    01234                 01234
    '''
    def clone(self):
        new_one = SEDirectionStrips(board_size=0, clone=True)
        new_one.strips = self.strips.__copy__()
        return new_one

    def get_bounds(self, s_num, board_size):
        # for board_size of 5:
        # strip 0 has min 0, max 0
        # strip 2 has min 0, max 2
        # strip 4 has min 0, max 4
        # strip 6 has min 2, max 4
        # strip 8 has min 4, max 4
        if s_num < board_size:
            return 0, s_num
        else:
            return s_num-board_size+1, board_size-1

    def set_up_strips(self, board_size):
        self.strips = a_m.array('L', [0]*(board_size*2))

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
        return (ind, s_num-ind)

    def get_occ(self, pos):
        return get_occ(self.get_strip(pos)[0], pos[0])

    def set_occ(self, pos, occ):
        bs, s_num = self.get_strip(pos)
        bs = self.get_strip(pos)[0]
        bs_new = set_occ(bs, pos[0], occ)
        self.strips[s_num] = bs_new
