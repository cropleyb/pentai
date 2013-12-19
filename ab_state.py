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
    def __init__(self, parent=None):
        if parent == None:
            self.utility_stats = UtilityStats()
            self.utility_calculator = UtilityCalculator()
        else:
            self.utility_stats = UtilityStats(parent.utility_stats)
            self.utility_calculator = parent.utility_calculator

    def reset_state(self):
        self.utility_stats = UtilityStats()

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

    # All the utility calculations belong in the UtilityCalculator
    # TODO: Cache stuff somehow?
    def utility(self):
        # The search_colour is the colour of the
        # AI player doing the search.
        # The turn_colour is the colour of the player to 
        # move at the leaf state of the search.
        # eval_colour is the colour that we are assessing
        # the utility value for -
        # we do both for each call to utility
        turn_colour = self.to_move_colour()
        search_colour = self.search_player_colour()
        other_colour = opposite_colour(turn_colour)

        # Check for immediate wins first, then forceable wins
        for win_eval_func in (self.zero_turn_win, self.one_turn_win):
            for eval_colour in (turn_colour, other_colour):
                eval_captured = self.state.get_all_captured()[eval_colour]
                eval_lines = self.utility_stats.lines[eval_colour]

                util, won = win_eval_func(
                    eval_lines, eval_captured, eval_colour, turn_colour)

                if won:
                    self.set_win_for(eval_colour)
                    if search_colour == eval_colour:
                        return util
                    else:
                        return -util

        # No forceable win has been found, so fudge up a score
        util_scores = [None, None, None]

        for eval_colour in (turn_colour, other_colour):
            eval_captured = self.state.get_all_captured()[eval_colour]
            eval_lines = self.utility_stats.lines[eval_colour]
            util = self.utility_score(
                    eval_lines,
                    eval_captured,
                    eval_colour, turn_colour)
            util_scores[eval_colour] = util

        # It is a very significant advantage to have the move
        util_scores[turn_colour] *= 100 

        if search_colour == turn_colour:
            return util_scores[turn_colour] - util_scores[other_colour]
        else:
            return util_scores[other_colour] - util_scores[turn_colour]

    def zero_turn_win(self, lines, captured, eval_colour, turn_colour):
        """ Detect a win in this position """
        if lines[4] > 0:
            # This position has been won already, mark it as such so
            # that the search is not continued from this node.
            self.state.set_won_by(eval_colour)
            return self.winning_score(), True

        rules = self.get_rules()
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        if sfcw > 0 and ccp:
            captured = self.state.get_all_captured()
            if captured[eval_colour] >= sfcw:
                # This position has been won already, mark it as such so
                # that the search is not continued from this node.
                self.state.set_won_by(eval_colour)
                return self.set_win_for(eval_colour), True

        return 0, False

    def one_turn_win(self, lines, captured, eval_colour, turn_colour):
        """ Detect a forceable win after one turn each """
        rules = self.get_rules()
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        if lines[3] > 0:
            if eval_colour == turn_colour:
                # An unanswered line of four out of five will win
                return self.winning_score() / 100, True

            if lines[3] > 1:
                # Two or more lines of four, with no danger of being
                # captured is a win.
                if ccp:
                    if self.get_takes()[opposite_colour(eval_colour)] == 0:
                        return self.winning_score() / 100, True

        if ccp and sfcw > 0:
            # Can win by captures
            if eval_colour == turn_colour:
                if (sfcw - captured) <= 2 and \
                        self.get_takes()[eval_colour] > 0:
                    # eval_colour can take the last pair for a win
                    return self.winning_score() / 100, True
            else:
                if (sfcw - captured) <= 2 and \
                        self.get_takes()[eval_colour] > 2:
                    # eval_colour can take the last pair for a win
                    return self.winning_score() / 100, True

        return 0, False

    def utility_score(self, lines, captured, eval_colour, turn_colour):
        """ Calculate a score for eval_colour for this state. """
        rules = self.get_rules()
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        score = 0

        for i in range(len(lines)):
            score *= 120
            rev = 4 - i
            score += lines[rev]

        if ccp:
            if sfcw > 0:
                cc = self.utility_calculator.captured_contrib(captured)
                score += cc
            # else: Captured stones are not worth anything

            # Give takes and threats some value for their ability to help
            # get 5 in a row.
            tc = self.utility_calculator.take_contrib(self.get_takes()[eval_colour])
            score += tc

            tc = self.utility_calculator.threat_contrib(self.get_threats()[eval_colour])
            score += tc

        return score

    def set_win_for(self, colour):
        return self.winning_score()

    # Scale these INFINITIES down to discourage sadistic
    # won game lengthening.
    def winning_score(self):
        # TODO: Sadistic mode for Rich - just multiply by move number ;)
        return INFINITY / self.state.get_move_number()

    # TODO: Rename to get_board
    def board(self):
        return self.state.board

    def get_rules(self):
        return self.game().rules

    def before_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs(self.board(), self.get_rules(), pos, -1)

    def after_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs(self.board(), self.get_rules(), pos, 1)

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

