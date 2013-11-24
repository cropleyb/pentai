
from pente_exceptions import *
from board import *

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

            # not + 1, that will be triggered by a move
            self.move_number = parent.move_number

            # TODO: copy AI observer manually
        self.last_move = "No move yet"

    def __repr__(self):
        # TEMP for debugging
        return str(self.last_move)
        #return self.game.__repr__()

    def get_board(self):
        return self.board

    def get_move_number(self):
        return self.move_number

    def get_captured(self, player_num):
        return self.captured[player_num]

    def get_all_captured(self):
        return self.captured

    # these two should only be used for testing
    def set_move_number(self, turn):
        self.move_number = turn

    def set_captured(self, player_num, pieces):
        self.captured[player_num] = pieces
    
    def make_move(self, move_pos):
        if self.board.off_board(move_pos):
            raise IllegalMoveException("That position is off the board")
        if self.board.get_occ(move_pos) > 0:
            raise IllegalMoveException("That position is already occupied")

        my_colour = self.to_move_colour()
        # Place a stone
        self.move_number += 1
        other_colour = self.to_move_colour()
        self.board.set_occ(move_pos, my_colour)
        board_size = self.board.get_size()

        MC = my_colour
        OC = other_colour

        # Process captures
        for ds in self.board.get_direction_strips():
            self.process_direction_captures(ds, move_pos, MC)

        # OLD. We only need to check for 5 in a row wins if we are not
        # an AI player - the AI data structure detects this already,
        # so it's duplicate work.

        # Check for a win by checking all the lines that run through
        # the move position.
        for ds in self.board.get_direction_strips():
            self.check_direction_for_5_in_a_row(ds, move_pos, my_colour)

        # TEMP for debugging
        self.last_move = move_pos

    def check_direction_for_5_in_a_row(self, ds, move_pos, my_colour):
        s, strip_num = ds.get_strip(move_pos)
        move_ind = ds.get_index(move_pos)
        if s.match_five_in_a_row(move_ind, my_colour):
            self.set_won_by(my_colour)

    def process_direction_captures(self, ds, move_pos, my_colour):
        captures = ds.get_captures(move_pos, my_colour)
        for capture_pos in captures:
            # Remove stone
            self.board.set_occ(capture_pos, EMPTY)

            # Keep track of capture count
            self.captured[my_colour] += 1
            if self.captured[my_colour] >= 10:
                self.set_won_by(my_colour)

    def set_won_by(self, wb):
        self._won_by = wb

    def get_won_by(self):
        return self._won_by

    def to_move_colour(self):
        return (self.move_number + 1) % 2 + 1 # BLACK is first on move 1
    
    def to_move_player(self):
        pn = (self.move_number + 1) % 2 # Player zero is BLACK
        return self.game.get_player(pn)

    def successors(self):
        succ = []
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                action = (x, y)
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

