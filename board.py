
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
        x,y = move_pos
        size = self.size
        return x < 0 or \
               x >= size or \
               y < 0 or \
               y >= size

    def get_occ(self, pos):
        colour_new = self.strips[0].get_occ(pos)
        # TEMP assertions 
        '''
        colour_new2 = self.strips[1].get_occ(pos)
        colour_new3 = self.strips[2].get_occ(pos)
        colour_new4 = self.strips[3].get_occ(pos)
        assert colour_new == colour_new2
        assert colour_new3 == colour_new4
        assert colour_new == colour_new3
        '''
        return colour_new

    def set_occ(self, pos, colour):
        for o in self.observers:
            o.before_set_occ(pos, colour)

        for s in self.strips:
            # We maintain the board position in four ways, update them all
            s.set_occ(pos, colour)

        for o in self.observers:
            o.after_set_occ(pos, colour)

