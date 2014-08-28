#!/usr/bin/python

import random
from pentai.base.defines import *

class UtilityCalculator(object):
    def __init__(self):
        pass

    def set_rules(self, rules):
        self.rules = rules

    """ Captures become increasingly important as we approach 5 """
    def captured_contrib(self, captures):
        contrib = captures * self.capture_score_base * \
                self.captures_scale[abs(captures/2)] # /2 for pairs
        # Unless we're playing keryo, captures_scale only needs to operate
        # on pairs
        return contrib

    def take_contrib(self, takes, captures):
        """ takes become increasingly important as we approach 5 captures """
        contrib = takes * self.take_score_base * \
                self.captures_scale[abs(captures/2)]
        return contrib

    def threat_contrib(self, threats, captures):
        """ threats become increasingly important as we approach 5 captures """
        contrib = threats * self.threat_score_base * \
                self.captures_scale[abs(captures/2)]
        return contrib

    def utility(self, state, utility_stats):
        """ This is the entry point into the position evaluation function """
        # us_copy = us_m.UtilityStats(utility_stats)
        # return self.utility_inner(state, utility_stats), us_copy
        val = self.utility_inner(state, utility_stats)
        try:
            mj = self.misjudgement
        except AttributeError:
            mj = self.misjudgement = 100 - self.judgement
        if mj > 0:
            val = 4 ** (random.random() * mj) * val
        return val

    def utility_inner(self, state, utility_stats):
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

        move_number = state.get_move_number()

        # Check for immediate wins first, then forceable wins
        for win_eval_func in (self.zero_turn_win, self.one_turn_win):
            for eval_colour in (turn_colour, other_colour):
                won = win_eval_func(state, eval_colour, turn_colour)

                if won:
                    # Scale these INFINITIES down to discourage sadistic
                    # won game lengthening.
                    if search_colour == eval_colour:
                        # If the winner is us then / by move number.
                        return INFINITY * 100 / (move_number*move_number)
                        # TODO: Sadistic mode for Rich
                        # - multiply by move number ;)
                    else:
                        # If the winner is not us then also / by move_number
                        return -INFINITY * 100 / (move_number*move_number)

        if utility_stats.lines == [None, [0,0,0,0,0], [0,0,0,0,0]] and \
                state.get_takes() == [0, 0, 0] and move_number > 30:
            # Draw
            state.set_won_by(P1 + P2)
            return 0

        # No forceable win has been found, so fudge up a score
        util_scores = [None, None, None]

        for eval_colour in (turn_colour, other_colour):
            util = self.utility_score(
                    state,
                    eval_colour, turn_colour)
            util_scores[eval_colour] = util

        # It is a very significant advantage to have the move
        util_scores[turn_colour] *= self.move_factor

        our_score = util_scores[turn_colour]
        their_score = util_scores[other_colour]

        if self.scale_pob and move_number < 10:
            # Scale by the pieces on the board (pob)
            eval_captured = state.get_captured(eval_colour)
            other_colour = opposite_colour(eval_colour)
            other_captured = state.get_captured(other_colour)
            our_pob = (1+move_number) / 2 - other_captured
            other_pob = (1+move_number) / 2 - eval_captured
            our_score *= our_pob
            their_score *= other_pob

        if self.calc_mode == 1:
            if search_colour == turn_colour:
                ret = our_score - their_score
            else:
                ret = their_score - our_score
        elif self.calc_mode == 2:
            # Unused
            if search_colour == turn_colour:
                ret = float(our_score) / (their_score or 1)
            else:
                ret = float(their_score) / (our_score or 1)
        else:
            # Unused
            assert self.calc_mode == 3
            both_scores = our_score + their_score
            if search_colour == turn_colour:
                ret = float(our_score - their_score) / both_scores
            else:
                ret = float(their_score - our_score) / both_scores

        return ret

    def zero_turn_win(self, state, eval_colour, turn_colour):
        """ Detect a win in this position """
        eval_captured = state.get_captured(eval_colour)
        eval_lines = state.utility_stats.lines[eval_colour]

        if eval_lines[4] > 0:
            # This position has been won already, mark it as such so
            # that the search is not continued from this node.
            # TODO: we shouldn't be modifying "state" here.
            state.set_won_by(eval_colour)
            return True

        rules = self.rules
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        if sfcw > 0 and ccp:
            if eval_captured >= sfcw:
                # This position has been won already, mark it as such so
                # that the search is not continued from this node.
                # TODO: we shouldn't be modifying "state" here.
                state.set_won_by(eval_colour)
                return True

        return False

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
                return True

            if eval_lines[3] > 1:
                # Two or more lines of four, with no danger of being
                # captured is a win.
                if ccp:
                    if state.get_takes()[opposite_colour(eval_colour)] == 0:
                        return True

        if ccp and sfcw > 0:
            # Can win by captures
            my_takes = state.get_takes()[eval_colour]
            if eval_colour == turn_colour:
                if (sfcw - eval_captured) <= 2 and my_takes > 0:
                    # eval_colour can take the last pair for a win
                    return True
            else:
                if (sfcw - eval_captured) <= 2 and my_takes > 2:
                    # eval_colour can take the last pair for a win
                    return True

        return False

    def utility_score(self, state, eval_colour, turn_colour):
        """ Calculate a score for eval_colour for this state. """
        rules = self.rules
        sfcw = rules.stones_for_capture_win
        ccp = rules.can_capture_pairs

        eval_captured = state.get_captured(eval_colour)
        other_colour = opposite_colour(eval_colour)
        other_captured = state.get_captured(other_colour)

        if self.use_net_captures:
            captured = eval_captured - other_captured
        else:
            captured = eval_captured

        score = 0

        lf = self.length_factor
        eval_lines = state.utility_stats.lines[eval_colour]
        # TODO: Use enumerate
        for i in range(len(eval_lines)):
            score *= lf
            rev = 4 - i
            score += eval_lines[rev] * self.length_scale[rev]

        if self.enclosed_four_base != 0:
            ee4 = state.utility_stats.enclosed_four[eval_colour]
            score += self.enclosed_four_base * ee4

        if ccp:
            if sfcw > 0:
                if captured != 0:
                    cc = self.captured_contrib(captured)
                    score += cc

                us = state.utility_stats

                # Give takes and threats some value for their ability to help
                # get 5 in a row.
                #tc = self.take_contrib(us.takes[eval_colour], net_captured)
                tc = self.take_contrib(us.takes[eval_colour], captured)
                score += tc

                #tc = self.threat_contrib(us.threats[eval_colour], net_captured)
                tc = self.threat_contrib(us.threats[eval_colour], captured)
                score += tc

            # else: Captured stones are not worth anything

        return score

