
# BOARD_SIZE = 7
DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
              (0,-1),(0,0),(0,1),
              (1,-1),(1,0),(1,1))

'''
class State():
    """ This is for the state of a game after a particular move. """
    def __init__(self, parent=None, move=None):
        self.parent = parent
        if parent == None:
            self.turn = 0
            self.captured = [0,0]
            # self.board = [[0 for k in range(BOARD_SIZE)] for l in range(BOARD_SIZE)]
            self.board_white = [0 for k in range(BOARD_SIZE)]
            self.board_black = [0 for k in range(BOARD_SIZE)]
            self.won_by = 0
            return
        # c = copy.deepcopy(parent)
        # self.__dict__ = c.__dict__
        # self.turn = self.turn + 1
        self.turn = parent.turn + 1
        self.captured = parent.captured[:]
        self.board_white = parent.board_white[:]
        self.board_black = parent.board_black[:]
        self.won_by = parent.won_by

        move_pos = move.position()
        if self.get_colour(move_pos) > 0:
            raise IllegalMoveException()

        # TODO: Check for whether this needs to be inverted?
        my_colour = self.turn % 2 + 1
        # Place a stone
        self.set_colour(move_pos, my_colour)

        # Process captures
        for direction in DIRECTIONS:
            clrs = self.colours(move_pos, direction, 4)
            if clrs == [1, 2, 2, 1] or clrs == [2, 1, 1, 2]:
                capture_pos1 = move_pos.shift(direction, 1)
                capture_pos2 = move_pos.shift(direction, 2)
                # Remove stones
                self.set_colour(capture_pos1, 0)
                self.set_colour(capture_pos2, 0)
                # Keep track of capture count
                self.captured[my_colour] += 1

        # Check for a win (TEMP)
        for direction in DIRECTIONS:
            l = 1
            while l < 5:
                test_pos = move_pos.shift(direction, l)
                if test_pos[0] < 0 or \
                   test_pos[0] >= BOARD_SIZE or \
                   test_pos[1] < 0 or \
                   test_pos[1] >= BOARD_SIZE:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.get_colour(test_pos)
                if next_col != my_colour:
                    break
                l += 1
            m = -1
            while m > -5:
                test_pos = move_pos.shift(direction, m)
                if test_pos[0] < 0 or \
                   test_pos[0] >= BOARD_SIZE or \
                   test_pos[1] < 0 or \
                   test_pos[1] >= BOARD_SIZE:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.get_colour(test_pos)
                if next_col != my_colour:
                    break
                m -= 1
            total_line_length = 1 + l - m
            if total_line_length >= 5:
                self.won_by = my_colour

    def to_move(self):
        return self.turn % 2

    def __repr__(self):
        edge = "* " * BOARD_SIZE
        board_array = ["\n" + edge]
        for y in range(BOARD_SIZE):
            line = []
            for x in range(BOARD_SIZE):
                ind = self.get_colour((x,y))
                col = " OX"[ind]
                line.append(col)
                line.append(' ')
            board_array.append("".join(line))
        board_array.append(edge)
        return "\n".join(board_array)

    def successors(self, state):
        succ = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                pos = (x, y)
                action = Move(pos)
                try:
                    succ.append((action, state.State(state, action)))
                except IllegalMoveException:
                    pass
        return succ

    def utility(self, player):
        # 5+ in a row or 5+ captured = infinity
        if self.captured[0] == 5 or self.won_by == 1:
            return alpha_beta.infinity
        if self.captured[1] == 5 or self.won_by == 2:
            return -alpha_beta.infinity
        return self.captured[0] - self.captured[1]


        # 4+ captured in pente rules
        # open 4
        # 2 + open 3s
        # closed 4
        # open 3
        # capture difference? pente rules
        # occupied positions (centre weighted)
        # closed 3s
        # subtract pairs
        # return 0 # state.utility()
'''

class Board():
    def __init__(self, size):
        self.size = size

    '''
    def get_colour(self, pos):
        # return self.board[pos[0]][pos[1]]
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        colour =           (self.board_black[y] & x_pos_bit) and 1
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
    '''

    def score(self):
        # TODO
        return 0

    def make_move(self, x, y):
        pass # TODO

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
