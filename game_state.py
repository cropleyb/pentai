
from board import *

# TODO: cloned in GUI
class IllegalMoveException(Exception):
    pass

DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
               (0,-1),        (0,1),
               (1,-1), (1,0), (1,1))

class Pos():
    def __init__(self, x, y):
        self.tup = (x,y)

    def __getitem__(self, dim):
        return self.tup[dim]

    def shift(self, direction, steps):
        new_pos = (self.tup[0] + (direction[0] * steps), \
                   self.tup[1] + (direction[1] * steps)) 
        return Pos(*new_pos)

    def __repr__(self):
        return str(self.tup)

    def __eq__(self, other):
        return self.tup == other.tup

class GameState():
    """ This is for the state of a game as of a particular move. """
    def __init__(self, game, parent=None, gui=None):
        self.game = game
        self.parent = parent
        self.gui = gui
        if parent == None:
            self.board = Board(game.size())
            self.captured = [0,0,0] # 3 for convenience
            self.won_by = False
            self.move_number = 1
        else:
            self.board = parent.board # TODO: Clone
            self.captured = parent.captured[:]
            self.won_by = parent.won_by
            self.move_number = parent.move_number #+ 1

    def get_move_number(self):
        return self.move_number

    def get_captured(self, player_num):
        return self.captured[player_num]

    # these two should only be used for testing
    def set_move_number(self, turn):
        self.move_number = turn

    def set_captured(self, player_num, pieces):
        self.captured[player_num] = pieces
    
    def make_move(self, move):
        move_pos = move.pos
        if self.board.get_occ(move_pos) > 0:
            raise IllegalMoveException("That position is already occupied")

        other_colour = self.to_move_colour()
        # Place a stone
        self.move_number += 1
        # FIXME: this should go before the move inc., but it breaks
        my_colour = self.to_move_colour()
        self.board.set_occ(move_pos, my_colour)
        board_size = self.board.get_size()

        if (self.gui != None):
            self.gui.place_stone(move_pos[0], move_pos[1], my_colour)

        MC = my_colour
        OC = other_colour

        # Process captures
        # TODO: keryo pente capture 3s
        for direction in DIRECTIONS:
            clrs = self.board.get_occs_in_a_line(move_pos, direction, 4)
            if clrs == [MC, OC, OC, MC]: # or clrs == [2, 1, 1, 2]:
                capture_pos1 = move_pos.shift(direction, 1)
                capture_pos2 = move_pos.shift(direction, 2)
                # Remove stones
                self.board.set_occ(capture_pos1, EMPTY)
                self.board.set_occ(capture_pos2, EMPTY)
                if (self.gui != None):
                    self.gui.remove_stone(capture_pos1[0], capture_pos1[1])
                    self.gui.remove_stone(capture_pos2[0], capture_pos2[1])
                # Keep track of capture count
                self.captured[my_colour] += 2

        # Check for a win (TEMP)
        # We only need half of the directions,
        # because for each we need to check the opposite direction
        for direction in DIRECTIONS[:4]:
            l = 1
            while l < 5:
                test_pos = move_pos.shift(direction, l)
                if test_pos[0] < 0 or \
                   test_pos[0] > board_size or \
                   test_pos[1] < 0 or \
                   test_pos[1] > board_size:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.board.get_occ(test_pos)
                if next_col != my_colour:
                    break
                l += 1
            m = -1
            while m > -5:
                test_pos = move_pos.shift(direction, m)
                if test_pos[0] < 0 or \
                   test_pos[0] > board_size or \
                   test_pos[1] < 0 or \
                   test_pos[1] > board_size:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.board.get_occ(test_pos)
                if next_col != my_colour:
                    break
                m -= 1
            total_line_length = 1 + (l-1) - (m+1)
            if total_line_length >= 5: # TODO: check rules for longer lines
                self.won_by = my_colour

    def to_move(self):
        return not self.move_number % 2

    def to_move_colour(self):
        return (self.move_number % 2) + 1

    def successors(self):
        succ = []
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                pos = Pos(x, y)
                action = Move(pos)
                try:
                    succ.append((action, State(self, action)))
                except IllegalMoveException:
                    pass
        return succ

    # TODO: Move this, use Rules object
    def utility(self, player):
        # 5+ in a row or 5+ pairs captured = infinity
        if self.captured[BLACK] >= 10 or self.won_by == BLACK:
            return alpha_beta.infinity
        if self.captured[WHITE] >= 10 or self.won_by == WHITE:
            return -alpha_beta.infinity
        return self.captured[0] - self.captured[1]

    def score(self):
        return self.utility(None)

