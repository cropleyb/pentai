#!/usr/bin/env python

import unittest

#from pentai.base.player import *
#import pentai.base.game_state
import pentai.base.board as b_m
from pentai.base.mock import *

from pentai.ai.length_lookup_table import *
import pentai.ai.ab_state as abs_m
import pentai.ai.utility_calculator as uc_m
import pentai.ai.utility_stats as us_m
import pentai.ai.priority_filter as pf_m # TODO: NullFilter
import pentai.ai.ai_genome as aig_m
import pentai.db.ai_factory as aif_m # Hmmm. Shouldn't need to use this here

import itertools

inf = INFINITY / 1000

class UtilityTest(unittest.TestCase):
    def setUp(self):

        self.search_filter = pf_m.PriorityFilter()
        self.util_calc = uc_m.UtilityCalculator()

        # Set defaults for utility calculation
        player = Mock({"get_utility_calculator":self.util_calc})
        genome = aig_m.AIGenome("Irrelevant")
        aif = aif_m.AIFactory()
        aif.set_utility_config(genome, player)

        self.s = abs_m.ABState(search_filter=self.search_filter,
                utility_calculator=self.util_calc)
        self.us = us_m.UtilityStats()
        self.rules = Mock()
        self.rules.stones_for_capture_win = 10
        self.rules.can_capture_pairs = True
        self.game = Mock()
        self.captured = [0, 0, 0] # This is individual stones, E/B/W
        self.gs = Mock({"get_all_captured": self.captured,
            "get_move_number": 10,
            "game":self.game,
            "get_won_by": EMPTY,
            "get_rules":self.rules}) 
        self.gs.board = b_m.Board(13)
        self.gs.game = self.game
        self.set_turn_player_colour(P1)
        self.set_search_player_colour(P1)
        self.s.set_state(self.gs)

    def utility(self):
        util = self.s.utility()
        return util

    def set_lines(self, pn, lines):
        us = self.s.utility_stats
        us.lines[pn] = lines

    def set_black_lines(self, lines):
        self.set_lines(P1, lines)

    def set_white_lines(self, lines):
        self.set_lines(P2, lines)

    def set_takes(self, black_takes, white_takes):
        self.s.utility_stats.takes = [0, black_takes, white_takes]

    def set_threats(self, black_threats, white_threats):
        self.s.utility_stats.threats = [0, black_threats, white_threats]

    def set_captured(self, black_captures, white_captures):
        self.captured[P1] = black_captures
        self.captured[P2] = white_captures

    def set_turn_player_colour(self, turn_player_colour):
        """ Set whose move it is at the leaf state """
        self.gs.mockAddReturnValues(to_move_colour=turn_player_colour)
        
    def set_search_player_colour(self, search_player_colour):
        """ Set whose move it is at the leaf state """
        self.game.mockAddReturnValues(to_move_colour=search_player_colour)

    def set_move_number(self, mn):
        self.gs.mockAddReturnValues(get_move_number=mn)
        
    def test_won_game_shortening(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)
        self.set_black_lines([0,0,0,4,0])

        self.set_move_number(10)
        u1 = self.utility()

        self.set_move_number(11)
        u2 = self.utility()
        self.assertGreater(u1, u2)

    def test_lost_game_lengthening(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)
        self.set_white_lines([0,0,0,4,0])

        self.set_move_number(10)
        u1 = self.utility()

        self.set_move_number(11)
        u2 = self.utility()
        self.assertGreater(u2, u1)

    # !python ./pentai/ai/t_utility.py UtilityTest.test_utility_single_stone_better_than_none
    def test_utility_single_stone_better_than_none(self):
        self.set_black_lines([20,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, 0)

    def test_utility_more_singles_is_better(self):
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, 0)

    def test_utility_more_twos_is_better(self):
        self.set_black_lines([0,1,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, 0)

    def test_utility_more_threes_is_better(self):
        self.set_black_lines([0,0,1,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, 0)

    def test_utility_more_fours_is_better(self):
        self.set_black_lines([0,0,0,1,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.utility()
        self.assertLess(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.utility()
        self.assertLess(u, 0)

    def test_utility_five_is_a_win(self):
        self.set_black_lines([0,0,0,0,1])
        self.set_white_lines([99,99,99,99,0])
        u = self.utility()
        self.assertGreaterEqual(u, inf)

    def test_black_win_by_captures(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(10, 0)
        u = self.utility()
        self.assertGreaterEqual(u, inf)

    def test_black_no_win_by_captures_for_five_in_a_row(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(10, 0)
        self.rules.stones_for_capture_win = 0
        u = self.utility()
        self.assertEqual(u, 0)

    def test_white_win_by_captures(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 10)
        u = self.utility()
        self.assertLessEqual(u, -inf)

    def test_white_no_win_by_captures_for_five_in_a_row(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 10)
        self.rules.stones_for_capture_win = 0
        u = self.utility()
        self.assertEqual(u, 0)

    def test_one_capture_worth_more_than_a_three(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.set_captured(2, 0)
        u = self.utility()
        self.assertGreaterEqual(u, 0)

    def test_one_capture_worth_less_than_a_four(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,1,0])
        self.set_turn_player_colour(P2)
        self.set_captured(2, 0)
        u = self.utility()
        self.assertLessEqual(u, 0)

    ######################

    def test_white_search(self):
        """ Search by white """
        self.set_search_player_colour(P2)
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        u = self.utility()
        self.assertGreaterEqual(u, 0)

    def test_white_capture(self):
        """ Search by white """
        self.set_search_player_colour(P2)
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 2)
        u = self.utility()
        self.assertGreaterEqual(u, 0)

    def test_black_to_move_advantage(self):
        """ Search by white """
        self.set_turn_player_colour(P1)
        self.set_search_player_colour(P2)
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.utility()
        self.assertLessEqual(u, 0)

    ###########

    def test_white_having_the_move_gets_a_higher_util(self):
        """ Search by white """
        self.set_search_player_colour(P2)

        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([2,0,0,0,0])

        self.set_turn_player_colour(P2)
        u_with_move = self.utility()

        self.set_turn_player_colour(P1)
        u_not_to_move = self.utility()

        self.assertGreater(u_with_move, u_not_to_move)

    def test_black_having_the_move_gets_a_higher_util(self):
        """ Search by black """
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([2,0,0,0,0])

        self.set_turn_player_colour(P1)
        u_with_move = self.utility()

        self.set_turn_player_colour(P2)
        self.set_search_player_colour(P1)
        u_not_to_move = self.utility()

        self.assertGreater(u_with_move, u_not_to_move)

    def test_next_to_middle_is_better(self):
        """ Search by white """
        self.set_turn_player_colour(P1)
        self.set_search_player_colour(P2)

        # (-783, [16, 0, 0, 0, 0][11, 0, 0, 0, 0] - (3, 3) next to 4,4
        self.set_black_lines([16,0,0,0,0])
        self.set_white_lines([11,0,0,0,0])
        u_adjacent = self.utility()

        # (-588, [17, 0, 0, 0, 0][7, 0, 0, 0, 0] - (6, 6) with a gap
        self.set_black_lines([17,0,0,0,0])
        self.set_white_lines([7,0,0,0,0])
        u_dist = self.utility()

        self.assertGreater(u_adjacent, u_dist)

    ##############

    def test_one_take_is_worth_more_than_a_few_pairs(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([11,3,0,0,0])
        self.set_takes(1, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def test_one_take_is_worth_more_than_two_threes(self):
        # I'm not sure about this one
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,2,0,0])
        self.set_takes(1, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def atest_one_take_is_worth_less_than_three_threes(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,3,0,0])
        self.set_takes(1, 0)
        u = self.utility()
        self.assertLess(u, 0)

    def test_one_take_with_the_move_is_worth_more_than_one_three(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.set_takes(1, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def test_one_three_with_the_move_is_worth_more_than_one_take(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.set_takes(1, 0)
        u = self.utility()
        self.assertLess(u, 0)

    def test_four_captures_worth_more_than_3_threes(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,3,0,0])
        self.set_captured(8, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def test_four_in_a_row_with_the_move_is_a_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_black_lines([0,0,0,1,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertGreater(u, inf)

    def test_four_in_a_row_without_the_move_is_not_won(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_black_lines([0,0,0,1,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.utility()
        self.assertLess(u, inf)

    def test_four_in_a_row_for_opposition_with_the_move_is_a_loss(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,1,0])
        u = self.utility()
        self.assertLess(u, -inf)

    def test_four_captures_and_a_threat_with_the_move_is_a_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_captured(8, 0)
        self.set_takes(1, 0)
        u = self.utility()
        self.assertGreater(u, inf)

    def test_four_captures_with_no_threats_with_the_move_is_not_a_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_captured(8, 0)
        self.set_takes(0, 0)
        u = self.utility()
        self.assertLess(u, inf)

    def test_four_captures_and_a_threat_for_oppenent_with_the_move_is_a_loss(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_captured(0, 8)
        self.set_takes(0, 1)
        u = self.utility()
        self.assertLess(u, -inf)

    def test_three_captures_and_a_threat_for_oppenent_with_the_move_is_not_a_loss(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_captured(0, 6)
        self.set_takes(0, 1)
        u = self.utility()
        self.assertGreater(u, -inf)

    def test_take_has_a_value(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_takes(1, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def test_threat_has_a_value(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_threats(1, 0)
        u = self.utility()
        self.assertGreater(u, 0)

    def test_two_fours_with_no_danger_of_being_captured_is_a_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_black_lines([0,0,0,2,0])
        self.set_takes(0, 0)
        u = self.utility()
        self.assertGreater(u, inf)

    def test_four_pairs_captured_and_three_takes_will_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_captured(8, 0)
        self.set_takes(3, 0)
        u = self.utility()
        self.assertGreater(u, inf)

    def atest_four_pairs_captured_and_three_takes_will_win(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_black_lines([0,0,3,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 2)
        self.set_takes(0, 0)

        u = self.utility()
        self.assertGreater(u, inf)

    ######################################################

    def test_tricky_pos_1(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P2)

        self.set_captured(4, 4)
        self.set_takes(0, 0)
        self.set_threats(0, 0)
        self.set_black_lines([78, 9, 1, 1, 0])
        self.set_white_lines([36, 2, 0, 0, 0])
        u1= self.utility()

        self.set_captured(0, 0)
        self.set_takes(0, 0)
        self.set_threats(2, 2)
        self.set_black_lines([51, 8, 0, 0, 0])
        self.set_white_lines([28, 3, 1, 0, 0])
        u2= self.utility()

        self.assertGreater(u1, u2)

    def test_tricky_pos_2(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_captured(0, 0)
        self.set_takes(0, 1)
        self.set_threats(0, 0)
        self.set_black_lines([34, 5, 1, 0, 0])
        self.set_white_lines([49, 6, 0, 0, 0])
        u1= self.utility()

        self.set_captured(2, 2)
        self.set_takes(0, 0)
        self.set_threats(2, 0)
        self.set_black_lines([49, 4, 0, 0, 0])
        self.set_white_lines([48, 5, 1, 0, 0])
        u2= self.utility()

        self.assertGreater(u1, u2)

    def test_strange(self):
        self.set_search_player_colour(P2)
        self.set_turn_player_colour(P2)

        self.set_captured(2, 2)
        self.set_takes(0, 0)
        self.set_threats(0, 0)
        self.set_black_lines([29, 2, 0, 0, 0])
        self.set_white_lines([33, 1, 0, 0, 0])
        u1= self.utility()

        self.set_captured(2, 0)
        self.set_takes(0, 1)
        self.set_threats(0, 0)
        self.set_black_lines([53, 3, 0, 0, 0])
        self.set_white_lines([24, 3, 0, 0, 0])
        u2= self.utility()

        self.assertGreater(u1, u2)

    def atest_tricky_pos_2b(self):
        # TODO
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        self.set_captured(2, 2)
        self.set_takes(0, 0)
        self.set_threats(0, 0)
        self.set_black_lines([59, 4, 0, 0, 0])
        self.set_white_lines([61, 3, 1, 0, 0])
        u1= self.utility()

        self.set_captured(2, 2)
        self.set_takes(0, 0)
        self.set_threats(2, 0)
        self.set_black_lines([49, 4, 0, 0, 0])
        self.set_white_lines([48, 5, 1, 0, 0])
        u2= self.utility()

        self.assertGreater(u1, u2)

    def test_yet_another(self):
        self.set_search_player_colour(P1)
        self.set_turn_player_colour(P1)

        '''
This should have got the highest score
((-55692, 0), ((9, 6), 14. Lines: [None, [38, 5, 0, 0, 0], [29, 0, 0, 0, 0]], Takes: [0, 0, 0], Threats: [0, 0, 2], Best: [{}, {}, {}] Captures: [0, 4, 4]))

But these all scored much higher
((33504, 0), ((5, 8), 14. Lines: [None, [35, 4, 0, 0, 0], [52, 1, 0, 0, 0]], Takes: [0, 1, 0], Threats: [0, 0, 2], Best: [{}, {}, {}] Captures: [0, 2, 4]))
((35313, 0), ((2, 2), 14. Lines: [None, [30, 4, 1, 0, 0], [56, 3, 0, 0, 0]], Takes: [0, 1, 0], Threats: [0, 0, 2], Best: [{}, {}, {}] Captures: [0, 2, 4]))
((36080, 0), ((9, 9), 14. Lines: [None, [35, 4, 1, 0, 0], [56, 3, 0, 0, 0]], Takes: [0, 1, 0], Threats: [0, 0, 2], Best: [{}, {}, {}] Captures: [0, 2, 4]))
((82186, 0), ((6, 7), 14. Lines: [None, [26, 8, 0, 0, 0], [49, 1, 0, 0, 0]], Takes: [0, 1, 0], Threats: [0, 0, 4], Best: [{}, {}, {}] Captures: [0, 2, 4]))

Utility for 14: (-22938, 0) (Lines: [None, [26, 8, 0, 0, 0], [49, 1, 0, 0, 0]], Takes: [0, 1, 0], Threats: [0, 0, 4], Best: NullFilter)
        '''
        self.set_captured(4, 4)
        self.set_takes(0, 0)
        self.set_threats(0, 2)
        self.set_move_number(14)
        self.set_black_lines([38, 5, 0, 0, 0])
        self.set_white_lines([29, 0, 0, 0, 0])
        u1= self.utility()

        self.set_captured(2, 4)
        self.set_takes(1, 0)
        self.set_threats(0, 4)
        self.set_black_lines([26, 8, 0, 0, 0])
        self.set_white_lines([49, 1, 0, 0, 0])
        u2= self.utility()

        self.assertGreater(u1, u2)

if __name__ == "__main__":
    unittest.main()



