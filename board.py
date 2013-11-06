
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
    def __init__(self, size):
        self.size = size
        self.board_white = [0 for k in range(size)]
        self.board_black = [0 for k in range(size)]

    def get_occ(self, pos):
        # return self.board[pos[0]][pos[1]]
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        colour =           (self.board_black[y] & x_pos_bit) and 1
        colour = colour or (self.board_white[y] & x_pos_bit) and 2
        return colour

    def set_occ(self, pos, colour):
        # self.board[pos[0]][pos[1]] = colour
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        if colour == 1:
            self.board_black[y] |= x_pos_bit
        elif colour == 2:
            self.board_white[y] |= x_pos_bit
        else:
            # clear
            self.board_black[y] &= ~x_pos_bit
            self.board_white[y] &= ~x_pos_bit

    # TODO - use yield, rename, combine L/R strands, reorder the left strand
    def colours(self, move_pos, direction, length):
        ''' Return a list of the colours of the stones in a line '''
        ret = []
        for distance in range(length):
            test_pos = self.shift(move_pos, direction, distance)
            if test_pos[0] < 0 or \
               test_pos[0] >= self.size or \
               test_pos[1] < 0 or \
               test_pos[1] >= self.size:
                # Other end of a potential capture is off the edge of the board
                continue
            ret.append(self.get_colour(test_pos))
        return ret
