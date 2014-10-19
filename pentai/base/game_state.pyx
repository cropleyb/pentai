
from pentai.base.pente_exceptions import *
from pentai.base.defines import *
import pentai.base.board as b_m
cimport pentai.base.board_strip as bs_m

class GameState(object):
    """ This is for the state of a game as of a particular move. 
    """
    def __init__(self, game, parent=None):
        self.game = game
        self.observers = []

        if parent == None:
            self.reset(game)
        else:
            self.board = parent.board.clone()
            self.captured = parent.captured[:]
            self.set_won_by(parent.get_won_by()) # TODO - EMPTY?

            # not + 1, that will be triggered by a move
            self.move_number = parent.move_number

        self.last_move = "No move yet"

    def __repr__(self):
        # For debugging
        return "%s. %s" % (self.move_number-1, self.last_move)

    def reset(self, game=None):
        if game is None:
            game = self.game
        self.board = b_m.Board(game.size())
        # 3 for convenience, should only use [1] and [2]
        self.captured = [0,0,0]
        self.set_won_by(EMPTY)
        self.move_number = 1
        for o in self.observers:
            o.reset_state(self)

    def get_rules(self):
        return self.game.rules

    def add_observer(self, o):
        if not o in self.observers:
            self.observers.append(o)

    def remove_observer(self, o):
        self.observers.remove(o)

    def get_board(self):
        return self.board

    def get_move_number(self):
        return self.move_number

    def get_captured(self, player_num):
        return self.captured[player_num]

    def get_all_captured(self):
        return self.captured

    def get_occ(self, pos):
        return self.board.get_occ(pos)

    # these two should only be used for testing
    def set_move_number(self, turn):
        self.move_number = turn

    def set_captured(self, player_num, pieces):
        self.captured[player_num] = pieces

    def set_occ(self, move_pos, my_colour):
        old_colour = self.board.get_occ(move_pos)

        for o in self.observers:
            o.before_set_occ(self.game, move_pos, old_colour)

        self.board.set_occ(move_pos, my_colour)

        for o in self.observers:
            o.after_set_occ(self.game, move_pos, my_colour)

    def is_illegal(self, move_pos):
        if self.board.off_board(move_pos):
            return OffBoardException("Position %s is off the board" % \
                    b_m.pos2str(move_pos))
        if self.board.get_occ(move_pos) > 0:
            return IllegalMoveException("Position %s is already occupied" % \
                    b_m.pos2str(move_pos))
        if self._won_by != EMPTY:
            return IllegalMoveException("The game is already over")

        if self.move_number == 3:
            rules = self.get_rules()
            if rules.move_is_too_close(move_pos):
                return IllegalMoveException("That move is too close to the centre.")
        return False

    def make_move(self, move_pos):
        exception = self.is_illegal(move_pos)
        if exception:
            raise exception

        rules = self.get_rules()

        my_colour = self.to_move_colour() # Save it before the turn is changed
        self.move_number += 1

        MC = my_colour
        OC = self.to_move_colour() # Other Colour

        ccp = rules.can_capture_pairs
        if ccp:
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
        if bs_m.match_five_in_a_row(s, move_ind, my_colour):
            self.set_won_by(my_colour)

    def process_direction_captures(self, ds, move_pos, my_colour):
        captures = ds.get_captures(move_pos, my_colour)
        for capture_pos in captures:
            # Remove stone
            self.set_occ(capture_pos, EMPTY)

            # Keep track of capture count
            self.captured[my_colour] += 1

            sfcw = self.get_rules().stones_for_capture_win
            if sfcw > 0:
                if self.captured[my_colour] >= sfcw:
                    self.set_won_by(my_colour)

    def set_won_by(self, wb):
        self._won_by = wb
        if wb:
            for ob in self.observers:
                ob.after_game_won(self.game, wb)

    def send_up_to_date(self):
        for ob in self.observers:
            ob.up_to_date(self.game)

    def get_won_by(self):
        return self._won_by

    def to_move_colour(self):
        return (self.move_number + 1) % 2 + 1 # P1 is first on move 1
    
    def to_move_player(self):
        pn = (self.move_number + 1) % 2 + 1 # Player 1 is P1, 2 P2
        return self.game.get_player(pn)

