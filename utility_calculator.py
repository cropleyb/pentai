#!/usr/bin/python

from defines import *

import pdb

class UtilityCalculator():
    def __init__(self):
        self.captured_score_base = 1500
        self.take_score_base = 350
        self.threat_score_base = 20
        self.captures_scale = [0, 2.0, 4.6, 10.0, 22.0, 46.0]

    def set_rules(self, rules):
        self.rules = rules

    """ Captures become increasingly important as we approach 5 """
    def captured_contrib(self, captures):
        # TODO: Use rules?
        contrib = captures * self.captured_score_base * \
                self.captures_scale[captures/2]
        return contrib

    def take_contrib(self, takes):
        """ TODO takes become increasingly important as we approach 5 captures """
        # TODO: Use rules?
        contrib = takes * self.take_score_base
        return contrib

    def threat_contrib(self, threats):
        """ TODO threats become increasingly important as we approach 5 captures """
        # TODO: Use rules?
        contrib = threats * self.threat_score_base
        return contrib

    # All the utility calculations belong in the UtilityCalculator
    # TODO: Cache stuff somehow?
    def utility(self, state, utility_stats):
        # The search_colour is the colour of the
        # AI player doing the search.
        # The turn_colour is the colour of the player to 
        # move at the leaf state of the search.
        # eval_colour is the colour that we are assessing
        # the utility value for -
        # we do both for each call to utility
        turn_colour = state.to_move_colour()
        search_colour = state.search_player_colour()
        other_colour = opposite_colour(turn_colour)

        # Check for immediate wins first, then forceable wins
        for win_eval_func in (self.zero_turn_win, self.one_turn_win):
            for eval_colour in (turn_colour, other_colour):
                util, won = win_eval_func(state, eval_colour, turn_colour)

                if won:
                    if search_colour == eval_colour:
                        return util
                    else:
                        return -util

        # No forceable win has been found, so fudge up a score
        util_scores = [None, None, None]

        for eval_colour in (turn_colour, other_colour):
            util = self.utility_score(
                    state,
                    eval_colour, turn_colour)
            util_scores[eval_colour] = util

        # It is a very significant advantage to have the move
        util_scores[turn_colour] *= 100 

        if search_colour == turn_colour:
            ret = util_scores[turn_colour] - util_scores[other_colour]
        else:
            ret = util_scores[other_colour] - util_scores[turn_colour]
        return ret

    def zero_turn_win(self, state, eval_colour, turn_colour):
        """ Detect a win in this position """
        eval_captured = state.get_captured(eval_colour)
        eval_lines = state.utility_stats.lines[eval_colour]

        if eval_lines[4] > 0:
            # This position has been won already, mark it as such so
            # that the search is not continued from this node.
            state.set_won_by(eval_colour)
            return self.winning_score(state), True

        rules = self.rules
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        if sfcw > 0 and ccp:
            if eval_captured >= sfcw:
                # This position has been won already, mark it as such so
                # that the search is not continued from this node.
                state.set_won_by(eval_colour)
                return self.winning_score(state), True

        return 0, False

    def one_turn_win(self, state, eval_colour, \
            turn_colour):
        """ Detect a forceable win after one turn each """
        rules = self.rules
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs
        eval_captured = state.get_captured(eval_colour)
        eval_lines = state.utility_stats.lines[eval_colour]

        if eval_lines[3] > 0:
            if eval_colour == turn_colour:
                # An unanswered line of four out of five will win
                return self.winning_score(state) / 100, True

            if eval_lines[3] > 1:
                # Two or more lines of four, with no danger of being
                # captured is a win.
                if ccp:
                    if state.get_takes()[opposite_colour(eval_colour)] == 0:
                        return self.winning_score(state) / 100, True

        if ccp and sfcw > 0:
            # Can win by captures
            my_takes = state.get_takes()[eval_colour]
            if eval_colour == turn_colour:
                if (sfcw - eval_captured) <= 2 and my_takes > 0:
                    # eval_colour can take the last pair for a win
                    return self.winning_score(state) / 100, True
            else:
                if (sfcw - eval_captured) <= 2 and my_takes > 2:
                    # eval_colour can take the last pair for a win
                    return self.winning_score(state) / 100, True

        return 0, False

    def utility_score(self, state, eval_colour, turn_colour):
        """ Calculate a score for eval_colour for this state. """
        rules = self.rules
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        eval_captured = state.get_captured(eval_colour)
        eval_lines = state.utility_stats.lines[eval_colour]

        score = 0

        for i in range(len(eval_lines)):
            score *= 120
            rev = 4 - i
            score += eval_lines[rev]

        if ccp:
            if sfcw > 0:
                cc = self.captured_contrib(eval_captured)
                score += cc
            # else: Captured stones are not worth anything

            us = state.utility_stats

            # Give takes and threats some value for their ability to help
            # get 5 in a row.
            tc = self.take_contrib(us.takes[eval_colour])
            score += tc

            tc = self.threat_contrib(us.threats[eval_colour])
            score += tc

        return score

    # Scale these INFINITIES down to discourage sadistic
    # won game lengthening.
    def winning_score(self, state):
        # TODO: Sadistic mode for Rich - just multiply by move number ;)
        return INFINITY / state.get_move_number()
