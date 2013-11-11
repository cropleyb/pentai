
from board import *
from pos import *

# TODO: cloned in GUI
class IllegalMoveException(Exception):
    pass

class GameState():
    """ This is for the state of a game as of a particular move. 
    """
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        if parent == None:
            self.board = Board(game.size())
            # 3 for convenience, should only use [1] and [2]
            self.captured = [0,0,0]
            self.set_won_by(False)
            self.move_number = 1
        else:
            self.board = parent.board.clone()
            self.captured = parent.captured[:]
            self.set_won_by(parent.get_won_by())
            self.move_number = parent.move_number # not + 1, that will be triggered by a move
            # TODO: copy AI observer manually

    def __repr__(self):
        return "TODO: game representation."
        #return self.game.__repr__()

    def get_board(self):
        return self.board

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

        MC = my_colour
        OC = other_colour

        # Process captures
        # TODO: keryo pente capture 3s
        for direction in DIRECTIONS:
            occs = self.board.get_occs_in_a_line_for_capture_test(move_pos, direction, 4)
            if occs == [MC, OC, OC, MC]:
                capture_pos1 = move_pos.shift(direction, 1)
                capture_pos2 = move_pos.shift(direction, 2)

                # Remove stones
                self.board.set_occ(capture_pos1, EMPTY)
                self.board.set_occ(capture_pos2, EMPTY)

                # Keep track of capture count
                self.captured[my_colour] += 2
                if self.captured[my_colour] >= 10:
                    self.set_won_by(MC)
                    #self.won_by = MC

        # Check for a win by checking all the lines that run through
        # the move position.
        # We only need to check half of the directions,
        # because for each we need to check the opposite direction
        # in case the last stone was not placed at an end.
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

            # Now see how far the line goes in the opposite direction.
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
            # TODO: check rules to see if lines longer than 5 also win
            if total_line_length >= 5:
                self.set_won_by(my_colour)

    def set_won_by(self, wb):
        self._won_by = wb

    def get_won_by(self):
        return self._won_by

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

    '''
    # TODO: Move this to ABState, maybe use Rules object
    def utility(self, player):
        # 5+ in a row or 5+ pairs captured = infinity
        if self.captured[BLACK] >= 10 or self.won_by == BLACK:
            return alpha_beta.infinity
        if self.captured[WHITE] >= 10 or self.won_by == WHITE:
            return -alpha_beta.infinity
        return self.captured[0] - self.captured[1]

    def score(self):
        return self.utility(None)
    '''

