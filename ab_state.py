#!/usr/bin/python

import board
import game_state
import alpha_beta
import game

from length_lookup_table import *
from utility_stats import *
from utility_calculator import *

class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None, search_filter=None):
        if parent == None:
            assert search_filter != None
            self.utility_stats = UtilityStats(search_filter=search_filter)
            self.utility_calculator = UtilityCalculator()
        else:
            self.utility_stats = UtilityStats(parent=parent.utility_stats)
            self.utility_calculator = parent.utility_calculator

    def reset_state(self):
        self.utility_stats = UtilityStats()

    # TODO: These don't belong here
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

    def get_captured(self, colour):
        return self.state.get_all_captured()[colour]

    def set_state(self, s):
        self.state = s
        # TODO: this should only need to be set once - it's referenced
        # by all states in a particular game
        self.utility_calculator.set_rules(s.get_rules())
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

    def utility(self):
        return self.utility_calculator.utility(self, self.utility_stats)

    # TODO: Rename to get_board
    def board(self):
        return self.state.board

    def get_rules(self):
        return self.game().rules

    def set_won_by(self, colour):
        self.state.set_won_by(colour)

    # TODO: Could these two be moved to utility_stats too?
    def before_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs( \
                self.board(), self.get_rules(), pos, -1)

    def after_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs( \
                self.board(), self.get_rules(), pos, 1)

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

