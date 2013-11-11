
from pos import *

EMPTY = 0
BLACK = 1
WHITE = 2

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
        self.board_black = array.array('L')
        self.board_black.extend([0] * (self.size + 1))

        self.board_white = array.array('L')
        self.board_white.extend([0] * (self.size + 1))
    
    def add_observer(self, o):
        self.observers.append(o)

    def clone(self):
        new_board = Board(self.size, clone_it=True)
        new_board.board_black = self.board_black.__copy__()
        new_board.board_white = self.board_white.__copy__()
        return new_board

    def get_size(self):
        return self.size

    def get_occ(self, pos):
        # return self.board[pos[0]][pos[1]]
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        colour =           (self.board_black[y] & x_pos_bit) and BLACK
        colour = colour or (self.board_white[y] & x_pos_bit) and WHITE
        return colour

    def set_occ(self, pos, colour):
        # self.board[pos[0]][pos[1]] = colour
        for o in self.observers:
            o.before_set_occ(pos, colour)

        y = pos[1]
        x_pos_bit = 1 << pos[0]
        if colour == BLACK:
            self.board_black[y] |= x_pos_bit
        elif colour == WHITE:
            self.board_white[y] |= x_pos_bit
        else:
            # clear
            self.board_black[y] &= ~x_pos_bit
            self.board_white[y] &= ~x_pos_bit

        for o in self.observers:
            o.after_set_occ(pos, colour)

    # TODO - use yield?
    def get_occs_in_a_line_for_capture_test(self, pos, direction, length):
        """ Return a list of the colours of the stones in a line 
            starting at 'pos'.
        """
        ret = []
        start_pos = pos # Pos(move[0], move[1])
        for distance in range(length):
            test_pos = start_pos.shift(direction, distance)
            if test_pos.off_board(self.size):
                # Other end of a potential capture is off the edge of the board
                continue
            # yield self.get_occ(test_pos)
            ret.append(self.get_occ(test_pos))
        return ret

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
