
#BOARD_SIZE = 13
BOARD_SIZE = 7
DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
              (0,-1),(0,0),(0,1),
              (1,-1),(1,0),(1,1))
#DIRECTIONS = ((1,0),)

class Board():
    def __init__(self, size):
        self.size = size

    def get_colour(self, pos):
        # return self.board[pos[0]][pos[1]]
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        colour =        (self.board_black[y] & x_pos_bit) and 1
        colour = colour or (self.board_white[y] & x_pos_bit) and 2
        return colour

    def set_colour(self, pos, colour):
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
               test_pos[0] >= BOARD_SIZE or \
               test_pos[1] < 0 or \
               test_pos[1] >= BOARD_SIZE:
                # Other end of a potential capture is off the edge of the board
                continue
            ret.append(self.get_colour(test_pos))
        return ret
