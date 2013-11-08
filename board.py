
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

    def __eq__(self, other):
        return self.tup[0] == other[0] and \
               self.tup[1] == other[1]

EMPTY = 0
BLACK = 1
WHITE = 2

class BoardObserver():
    def set_occ(self, pos, colour):
        pass

class Board():
    def __init__(self, size):
        self.size = size
        self.board_black = [0 for k in range(size+1)]
        self.board_white = [0 for k in range(size+1)]
        self.observers = []
    
    def add_observer(self, o):
        self.observers.append(o)

    def clone(self):
        new_board = Board(self.size, self.gui)
        new_board.board_black = self.board_black[:]
        new_board.board_white = self.board_white[:]

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

        for o in self.observers:
            o.set_occ(pos, colour)

    # TODO - use yield?
    def get_occs_in_a_line_for_capture_test(self, move, direction, length):
        """ Return a list of the colours of the stones in a line 
            starting at 'move'.
        """
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
            if test_pos[0] < 0 or \
               test_pos[0] >= self.size or \
               test_pos[1] < 0 or \
               test_pos[1] >= self.size:
                # off the edge of the board
                continue
            # yield self.get_occ(test_pos)
            ret.append(test_pos)
        return ret
