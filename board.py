
from pos import *
from direction_strips import *
from pente_exceptions import *

class BoardObserver():
    def before_set_occ(self, pos, colour):
        pass

    def after_set_occ(self, pos, colour):
        pass

import array

class Board():
    def __init__(self, size, clone_it=False):
        self.size = size
        self.observers = []
        if not clone_it:
            self.set_to_empty()

    def set_to_empty(self):
        self.strips = []
        self.strips.append(EDirectionStrips(self.size))
        self.strips.append(SEDirectionStrips(self.size))
        self.strips.append(SDirectionStrips(self.size))
        self.strips.append(SWDirectionStrips(self.size))

    def get_direction_strips(self):
        return self.strips
    
    def add_observer(self, o):
        self.observers.append(o)

    def clone(self):
        new_board = Board(self.size, clone_it=True)
        new_board.strips = [s.clone() for s in self.strips]
        return new_board

    def get_size(self):
        return self.size

    def off_board(self, move_pos):
        return move_pos.off_board(self.size)

    def get_occ(self, pos):
        colour_new = self.strips[0].get_occ(pos)

        # TEMP tests
        colour_new2 = self.strips[1].get_occ(pos)
        colour_new3 = self.strips[2].get_occ(pos)
        colour_new4 = self.strips[3].get_occ(pos)
        assert colour_new == colour_new2
        assert colour_new3 == colour_new4
        assert colour_new == colour_new3
        
        return colour_new

    def set_occ(self, pos, colour):
        for o in self.observers:
            o.before_set_occ(pos, colour)

        for s in self.strips:
            # We maintain the board position in four ways, update them all
            s.set_occ(pos, colour)

        for o in self.observers:
            o.after_set_occ(pos, colour)

    def get_positions_in_line_through_pos(self, pos, direction, length):
        """ Return a list of the colours of the stones in a line 
            going through 'pos', 'length' in each direction.
        """
        ret = []
        start_pos = pos.shift(direction, -length)
        for distance in range(1 + 2*length):
            test_pos = start_pos.shift(direction, distance)
            if test_pos.off_board(self.size):
                continue
            # yield test_pos
            ret.append(test_pos)
        return ret
