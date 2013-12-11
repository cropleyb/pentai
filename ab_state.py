#!/usr/bin/python

import board
import game_state
import alpha_beta
import game
from board_strip import *

from length_lookup_table import *
from take_counter import *
from threat_counter import *
from utility_stats import *

import pdb

CAPTURED_SCORE_BASE = 120 ** 3
TAKE_SCORE_BASE = 350
THREAT_SCORE_BASE = 20
CAPTURES_SCALE = [0, 2.0, 4.6, 10.0, 22.0, 46.0]

class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None):
        if parent == None:
            self.utility_stats = UtilityStats()
        else:
            self.utility_stats = UtilityStats(parent.utility_stats)

    def get_black_line_counts(self):
        return self.utility_stats.lines[BLACK]

    def get_white_line_counts(self):
        return self.utility_stats.lines[WHITE]

    def get_takes(self):
        return self.utility_stats.takes

    def get_threats(self):
        return self.utility_stats.threats

    def get_iter(self, to_move):
        return self.utility_stats.search_filter

    def set_state(self, s):
        self.state = s
        s.add_observer(self)

    def to_move_colour(self):
        return self.state.to_move_colour()

    def get_move_number(self):
        return self.state.get_move_number()

    def to_move(self):
        """ This is only to keep the AB code unchanged; the value is unused. """
        return None

    def search_player_colour(self):
        """ The AI player who is performing the search """
        game = self.game()
        return game.to_move_colour()

    # TODO?
    def __repr__(self):
        return ""

    def game(self):
        return self.state.game

    # TODO: Cache stuff somehow?
    def utility(self):
        """ The search_colour is the colour of the AI player doing the search """
        # The turn_colour is the colour of the player to move at the leaf state
        # of the search.
        turn_colour = self.to_move_colour()
        search_colour = self.search_player_colour()

        black_contrib = self.utility_contrib(self.get_black_line_counts(), BLACK)
        white_contrib = self.utility_contrib(self.get_white_line_counts(), WHITE)

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
        # Scale these INFINITIES down to discourage sadistic
        # won game lengthening.
        if captured[colour] >= 10:
            return INFINITY / self.state.get_move_number()

        if lines[4] > 0:
            return INFINITY / self.state.get_move_number()

        # No win by "colour" found, fudge up a score
        score = 0

        for i in range(len(lines)):
            score *= 120
            rev = 4 - i
            score += lines[rev]

        cc = self.captured_contrib(captured[colour])
        score += cc

        tc = self.take_contrib(self.get_takes()[colour])
        score += tc

        tc = self.threat_contrib(self.get_threats()[colour])
        score += tc

        #print "black: %s, white: %s, score: %s" % (self.black_lines, self.white_lines, \
        #        score)
        return score

    """ Captures become increasingly important as we approach 5 """
    def captured_contrib(self, captures):
        # TODO: Use rules
        contrib = captures * CAPTURED_SCORE_BASE * CAPTURES_SCALE[captures/2]
        return contrib

    def take_contrib(self, takes):
        """ TODO takes become increasingly important as we approach 5 captures """
        # TODO: Use rules
        contrib = takes * TAKE_SCORE_BASE
        return contrib

    def threat_contrib(self, threats):
        """ TODO threats become increasingly important as we approach 5 captures """
        # TODO: Use rules
        contrib = threats * THREAT_SCORE_BASE
        return contrib

    def board(self):
        return self.state.board

    def before_set_occ(self, pos, colour):
        self._set_or_reset_occs(pos, -1)

    def after_set_occ(self, pos, colour):
        self._set_or_reset_occs(pos, 1)

    def _set_or_reset_occs(self, pos, inc):
        # update substrips
        brd = self.board()
        for ds in brd.get_direction_strips():
            # Keep track of the lengths of lines that can form 5
            # in a row
            brd_size = brd.get_size()

            bs, s_num = ds.get_strip(pos)
            ind = ds.get_index(pos)

            strip_min, strip_max = ds.get_bounds(s_num, brd_size)

            # These are the absolute indices that bound the strip
            # we want to use to adjust length stats.
            min_ind = max(strip_min, ind-4) # TODO: constants
            max_ind = min(ind+4, strip_max) # inclusive

            us = self.utility_stats
            us.set_ind_to_pos(ds.get_pos, s_num)

            process_substrips(bs, min_ind, max_ind, us, inc)

            # TODO: brd_size may need changing due to some diagonal captures?
            process_takes(bs, ind, brd_size, us, inc)
            process_threats(bs, ind, brd_size, us, inc)

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

