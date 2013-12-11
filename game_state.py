
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
            self.observers = []
        else:
            self.board = parent.board.clone()
            self.captured = parent.captured[:]
            self.set_won_by(parent.get_won_by())

            # not + 1, that will be triggered by a move
            self.move_number = parent.move_number

            self.observers = []

        self.last_move = "No move yet"

    def __repr__(self):
        # TEMP for debugging
        return str(self.last_move)
        #return self.game.__repr__()

    def add_observer(self, o):
        self.observers.append(o)

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

    def set_occ(self, move_pos, my_colour):
        self.board.set_occ(move_pos, my_colour, self.observers)

    def make_move(self, move_pos):
        if self.board.off_board(move_pos):
            raise IllegalMoveException("That position is off the board")
        if self.board.get_occ(move_pos) > 0:
            raise IllegalMoveException("Position %s is already occupied" % \
                    (move_pos,))
        if self._won_by != EMPTY:
            raise IllegalMoveException("The game is already over")

        my_colour = self.to_move_colour() # Save it before the turn is changed
        self.move_number += 1

        MC = my_colour
        OC = self.to_move_colour() # Other Colour

        # Process captures
        for ds in self.board.get_direction_strips():
            self.process_direction_captures(ds, move_pos, MC)

        # Place a stone
        self.set_occ(move_pos, my_colour)

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
            self.set_occ(capture_pos, EMPTY)

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
        pn = (self.move_number + 1) % 2 + 1 # Player 1 is BLACK, 2 WHITE
        return self.game.get_player(pn)

