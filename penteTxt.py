#!/usr/bin/python
import pdb
import alpha_beta

# TODO
#BOARD_SIZE = 13
BOARD_SIZE = 7
DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
              (0,-1),(0,0),(0,1),
              (1,-1),(1,0),(1,1))
#DIRECTIONS = ((1,0),)

class Move():
    def __init__(self, pos):
        self.pos = pos
    def position(self):
        return self.pos

class IllegalMoveException(Exception):
    pass

import copy

class Board():
    def __init__(self, size):
        self.size = size

'''
class UtilityStats():
    def __init__(self, parent_stats=None):
        if parent_stats == None:
            self.captured = [0,0]
            # 5s
            # open 4s
            # half open 4s
            # closed 4s
            # open 3s
            # half open 3s
            # open 2s
            # threatened 2s
            # safe 2s?
            # open 1s
        self.captured = parent_stats.captured[:]

    # 5+ in a row or 5+ captured = infinity
    if state.captured[0] == 5:
        return infinity
    if state.captured[1] == 5:
        return -infinity
    return state.captured[0] - state.captured[1]
    # 4+ captured in pente rules
    # open 4
    # 2 + open 3s
    # closed 4
    # open 3
    # capture difference? pente rules
    # occupied positions (centre weighted)
    # closed 3s
    # subtract pairs
'''

class Pos():
    def __init__(self, x, y):
        self.tup = (x,y)
    def __getitem__(self, dim):
        return self.tup[dim]

class State():
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
                capture_pos1 = self.shift(move_pos, direction, 1)
                capture_pos2 = self.shift(move_pos, direction, 2)
                # Remove stones
                self.set_colour(capture_pos1, 0)
                self.set_colour(capture_pos2, 0)
                # Keep track of capture count
                self.captured[my_colour] += 1

        # Check for a win (TEMP)
        for direction in DIRECTIONS:
            l = 1
            while l < 5:
                test_pos = self.shift(move_pos, direction, l)
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
                test_pos = self.shift(move_pos, direction, m)
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

    def get_colour(self, pos):
        # return self.board[pos[0]][pos[1]]
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        col =        (self.board_black[y] & x_pos_bit) and 1
        col = col or (self.board_white[y] & x_pos_bit) and 2
        return col

    def set_colour(self, pos, col):
        # self.board[pos[0]][pos[1]] = col
        y = pos[1]
        x_pos_bit = 1 << pos[0]
        if col == 1:
            self.board_black[y] |= x_pos_bit
        elif col == 2:
            self.board_white[y] |= x_pos_bit
        else:
            # clear
            self.board_black[y] &= ~x_pos_bit
            self.board_white[y] &= ~x_pos_bit

    # TODO: move to pos
    def shift(self, pos, direction, steps):
        new_pos = (pos[0] + (direction[0] * steps), \
                   pos[1] + (direction[1] * steps)) 
        return new_pos

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

    def score(self):
        return self.utility(None)


class Game():
    def __init__(self, size):
        self.board = Board(size)
        # TEMP HACK
        global BOARD_SIZE
        BOARD_SIZE = size
        self.current_state = State()
        #pdb.set_trace()

    def to_move(self, state):
        return state.to_move()

    def make_move(self, x, y):
        self.current_state.set_colour(Pos(x,y), 1)

    def utility(self, state, player):
        return state.utility(player)


    def successors(self, state):
        succ = []
        #pdb.set_trace()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                pos = (x, y)
                action = Move(pos)
                try:
                    succ.append((action, State(state, action)))
                except IllegalMoveException:
                    pass
        return succ

    def terminal_test(self, state):
        return False
        # return len(self.successors(state)) == 0 THIS causes mass delay

if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    g = Game(7)

    #pdb.set_trace()
    alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
