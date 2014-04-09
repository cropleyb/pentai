
import pentai.base.direction_strips as ds_m
from pentai.base.pente_exceptions import *
from pentai.base.defines import *

class Board(object):
    def __init__(self, size, clone_it=False):
        self.size = size
        if not clone_it:
            self.set_to_empty()

    def set_to_empty(self):
        self.d_strips = []
        self.d_strips.append(ds_m.EDirectionStrips(self.size))
        self.d_strips.append(ds_m.SEDirectionStrips(self.size))
        self.d_strips.append(ds_m.SDirectionStrips(self.size))
        self.d_strips.append(ds_m.SWDirectionStrips(self.size))

    def key(self):
        k = 0
        estrips = self.d_strips[0]
        for s in estrips.strips:
            k += s
            k *= 4 ** self.size
        return k

    def get_direction_strips(self):
        return self.d_strips
    
    def clone(self):
        new_board = Board(self.size, clone_it=True)
        new_board.d_strips = [s.clone() for s in self.d_strips]
        return new_board

    def __repr__(self):
        size = self.size
        rep = '\n'
        for j in range(size-1,-1,-1):
            line = [ ['.','B','W'][self.d_strips[0].get_occ((i,j))] for i in range(size) ]
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
        colour = self.d_strips[0].get_occ(pos)
        return colour

    def set_occ(self, pos, colour):
        if self.off_board(pos):
            raise OffBoardException

        for s in self.d_strips:
            # We maintain the board position in four ways, update them all
            s.set_occ(pos, colour)

