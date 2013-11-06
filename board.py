
# BOARD_SIZE = 7
DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
              (0,-1),(0,0),(0,1),
              (1,-1),(1,0),(1,1))

class Pos():
    def __init__(self, x, y):
        self.tup = (x,y)
    def __getitem__(self, dim):
        return self.tup[dim]
    def shift(self, direction, steps):
        new_pos = (self.tup[0] + (direction[0] * steps), \
                   self.tup[1] + (direction[1] * steps)) 
        return Pos(*new_pos)

EMPTY = 0
BLACK = 1
WHITE = 2

class Board():
    def __init__(self, size, gui=None):
        self.size = size
        self.board_white = [0 for k in range(size+1)]
        self.board_black = [0 for k in range(size+1)]
        self.gui = gui

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

    # TODO - use yield, rename, combine L/R strands, reorder the left strand
    def get_occs_in_a_line(self, move, direction, length):
        """ Return a list of the colours of the stones in a line """
        ret = []
        start_pos = Pos(move[0], move[1])
        for distance in range(length):
            test_pos = start_pos.shift(direction, distance)
            if test_pos[0] < 0 or \
               test_pos[0] >= self.size or \
               test_pos[1] < 0 or \
               test_pos[1] >= self.size:
                # Other end of a potential capture is off the edge of the board
                continue
            ret.append(self.get_occ(test_pos))
        return ret
