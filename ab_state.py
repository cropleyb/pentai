#!/usr/bin/python

import board
import game_state
import alpha_beta
import nearby_filter
import game
import gui
from board_strip import *

from length_counter import *
from take_counter import *

import pdb

CAPTURE_SCORE_BASE = 120 ** 3
TAKE_SCORE_BASE = 190


class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None):
        if parent == None:
            self.black_lines = LengthCounter()
            self.white_lines = LengthCounter()
            self.takes = [0, 0, 0]
            self.search_filter = None
        else:
            self.black_lines = LengthCounter(parent.black_lines) # TODO: clone method
            self.white_lines = LengthCounter(parent.white_lines)
            self.takes = parent.takes[:]
            self.search_filter = parent.search_filter.clone()

    def get_black_line_counts(self):
        return self.black_lines

    def get_white_line_counts(self):
        return self.white_lines

    def get_iter(self):
        return self.search_filter

    def set_state(self, s):
        self.state = s
        self.board().add_observer(self)
        if self.search_filter is None:
            self.search_filter = nearby_filter.NearbyFilter(self.board())
        # TODO: Remove us as an observer from previous self.state?

    def to_move_colour(self):
        return self.state.to_move_colour()

    def to_move(self):
        """ This is only to keep the AB code unchanged; the value is unused. """
        return None

    def __repr__(self):
        ret = str(self.black_lines) + str(self.white_lines) + self.state.__repr__()
        return ret

    def search_player_colour(self):
        """ The AI player who is performing the search """
        game = self.game()
        return game.to_move_colour()

    def game(self):
        return self.state.game

    # TODO: Cache stuff somehow?
    def utility(self, unused=None):
        """ The search_colour is the colour of the AI player doing the search """
        # The turn_colour is the colour of the player to move at the leaf state
        # of the search.
        turn_colour = self.to_move_colour()
        search_colour = self.search_player_colour()

        black_contrib = self.utility_contrib(self.black_lines, BLACK)
        white_contrib = self.utility_contrib(self.white_lines, WHITE)

        # Having the move is worth a lot.
        if turn_colour == BLACK:
            black_contrib *= 100
        else:
            white_contrib *= 100

        #print "B/W contrib: %s, %s, %s" % (black_contrib, white_contrib, self)
        if search_colour == BLACK:
            return black_contrib - white_contrib
        else:
            return white_contrib - black_contrib

    def utility_contrib(self, lines, colour):
        # Check for a win first
        # TODO: check rules
        captured = self.state.get_all_captured()
        if captured[colour] >= 10:
            return alpha_beta.infinity

        if lines[4] > 0:
            return alpha_beta.infinity

        # No win by "colour" found, fudge up a score
        score = 0

        for i in range(len(lines)):
            score *= 100
            rev = 4 - i
            score += lines[rev]

        cc = self.captured_contrib(captured[colour])
        score += cc

        tc = self.take_contrib(self.takes[colour])
        score += tc

        #print "black: %s, white: %s, score: %s" % (self.black_lines, self.white_lines, \
        #        score)
        return score

    def captured_contrib(self, captures):
        """ TODO captures become increasingly important as we approach 5 """
        # TODO: Use rules
        contrib = captures * CAPTURE_SCORE_BASE
        return contrib

    def take_contrib(self, takes):
        """ TODO takes become increasingly important as we approach 5 captures """
        # TODO: Use rules
        contrib = takes * TAKE_SCORE_BASE
        return contrib

    def board(self):
        return self.state.board

    def before_set_occ(self, pos, colour):
        self._set_or_reset_occs(pos, -1)

    def after_set_occ(self, pos, colour):
        self._set_or_reset_occs(pos, 1)
        # Update the move filtering
        if colour == EMPTY:
            self.search_filter.capture(pos)
        else:
            self.search_filter.move(pos)

    def _set_or_reset_occs(self, pos, inc):
        # update substrips
        brd = self.board()
        for ds in brd.get_direction_strips():
            # Keep track of the lengths of lines that can form 5
            # in a row
            brd_size = brd.get_size()

            ca = CandidateAccumulator() # TEMP HACK

            bs, s_num = ds.get_strip(pos)
            ind = ds.get_index(pos)

            strip_min, strip_max = ds.get_bounds(s_num, brd_size)

            # These are the absolute indices that bound the strip
            # we want to use to adjust length stats.
            min_ind = max(strip_min, ind-4) # TODO: constants
            max_ind = min(ind+4, strip_max) # inclusive

            length_counters = [None, self.black_lines, self.white_lines]
            process_substrips(bs, min_ind, max_ind, 
                    ca, length_counters, inc)

            # TODO: brd_size may need changing due to some diagonal captures?
            process_takes(bs, ind, brd_size, self.takes, inc)

    def create_state(self, move_pos):
        ab_child = ABState(self)

        # clone the base level state object
        base_child = game_state.GameState(self.state.game, self.state)

        # connect the two (including move hook)
        ab_child.set_state(base_child)

        # make the move for the base (which updates ab_child)
        base_child.make_move(move_pos)

        return ab_child

    def terminal(self):
        return self.state.get_won_by() != game.EMPTY

