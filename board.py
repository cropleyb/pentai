
from direction_strips import *
from pente_exceptions import *

import array

class Board():
    def __init__(self, size, clone_it=False):
        self.size = size
        if not clone_it:
            self.set_to_empty()

    def set_to_empty(self):
        self.strips = [] # TODO Rename to d_strips
        self.strips.append(EDirectionStrips(self.size))
        self.strips.append(SEDirectionStrips(self.size))
        self.strips.append(SDirectionStrips(self.size))
        self.strips.append(SWDirectionStrips(self.size))

    def get_direction_strips(self):
        return self.strips
    
    def clone(self):
        new_board = Board(self.size, clone_it=True)
        new_board.strips = [s.clone() for s in self.strips]
        return new_board

    def __repr__(self):
        size = self.size
        rep = '\n'
        for j in range(size-1,-1,-1):
            line = [ ['.','B','W'][self.strips[0].get_occ((i,j))] for i in range(size) ]
            rep = rep + ' '.join(line) + '\n'
        return rep
 
    def get_size(self):
        return self.size

    def off_board(self, pos):
        x,y = pos
        size = self.size
        return x < 0 or \
               x >= size or \
               y < 0 or \
               y >= size

    def get_occ(self, pos):
        if self.off_board(pos):
            raise OffBoardException
        colour_new = self.strips[0].get_occ(pos)
        return colour_new

    def set_occ(self, pos, colour, observers=()):
        if self.off_board(pos):
            raise OffBoardException

        for o in observers:
            o.before_set_occ(pos, colour)

        for s in self.strips:
            # We maintain the board position in four ways, update them all
            s.set_occ(pos, colour)

        for o in observers:
            o.after_set_occ(pos, colour)

