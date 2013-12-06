#!/usr/bin/env python

import unittest

from length_lookup_table import *
from ab_state import *
from player import *
import game_state
from board import *
from mock import *

inf = alpha_beta.infinity / 2

import pdb

class UtilityTest(unittest.TestCase):
    def setUp(self):
        self.s = ABState()
        self.game = Mock()
        self.captured = [0, 0, 0]
        self.gs = Mock({"get_all_captured": self.captured}) 
        self.gs.board = Board(13)
        self.gs.game = self.game
        self.set_turn_player_colour(BLACK)
        self.set_search_player_colour(BLACK)
        self.s.set_state(self.gs)

    def set_black_lines(self, lines):
        self.s.utility_stats.lines[BLACK] = lines

    def set_white_lines(self, lines):
        self.s.utility_stats.lines[WHITE] = lines

    def set_captured(self, black_captures, white_captures):
        self.captured[BLACK] = black_captures
        self.captured[WHITE] = white_captures

    def set_turn_player_colour(self, turn_player_colour):
        """ Set whose move it is at the leaf state """
        self.gs.mockAddReturnValues(to_move_colour=turn_player_colour)
        
    def set_search_player_colour(self, search_player_colour):
        """ Set whose move it is at the leaf state """
        self.game.mockAddReturnValues(to_move_colour=search_player_colour)
        
    def test_utility_single_stone_better_than_none(self):
        self.set_black_lines([20,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_utility_more_singles_is_better(self):
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_utility_more_twos_is_better(self):
        self.set_black_lines([0,1,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_utility_more_threes_is_better(self):
        self.set_black_lines([0,0,1,0,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_utility_more_fours_is_better(self):
        self.set_black_lines([0,0,0,1,0])
        self.set_white_lines([0,0,0,0,0])
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.s.utility()
        self.assertLess(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.s.utility()
        self.assertLess(u, 0)

    def test_utility_five_is_a_win(self):
        self.set_black_lines([0,0,0,0,1])
        self.set_white_lines([99,99,99,99,0])
        u = self.s.utility()
        self.assertGreaterEqual(u, inf)

    def test_black_win_by_captures(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(10, 0)
        u = self.s.utility()
        self.assertGreaterEqual(u, inf)

    def test_white_win_by_captures(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 10)
        u = self.s.utility()
        self.assertLessEqual(u, -inf)

    def test_one_capture_worth_more_than_a_three(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.set_captured(1, 0)
        u = self.s.utility()
        self.assertGreaterEqual(u, 0)

    def test_one_capture_worth_less_than_a_four(self):
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,1,0])
        self.set_turn_player_colour(WHITE)
        self.set_captured(1, 0)
        u = self.s.utility()
        self.assertLessEqual(u, 0)

    ######################

    def test_white_search(self):
        """ Search by white """
        self.set_search_player_colour(WHITE)
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        u = self.s.utility()
        self.assertGreaterEqual(u, 0)

    def test_white_capture(self):
        """ Search by white """
        self.set_search_player_colour(WHITE)
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,0,0,0])
        self.set_captured(0, 1)
        u = self.s.utility()
        self.assertGreaterEqual(u, 0)

    def test_black_to_move_advantage(self):
        """ Search by white """
        self.set_turn_player_colour(BLACK)
        self.set_search_player_colour(WHITE)
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([1,0,0,0,0])
        u = self.s.utility()
        self.assertLessEqual(u, 0)

    ###########

    def test_white_having_the_move_gets_a_higher_util(self):
        """ Search by white """
        self.set_search_player_colour(WHITE)

        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([2,0,0,0,0])

        self.set_turn_player_colour(WHITE)
        u_with_move = self.s.utility()

        self.set_turn_player_colour(BLACK)
        u_not_to_move = self.s.utility()

        self.assertGreater(u_with_move, u_not_to_move)

    def test_black_having_the_move_gets_a_higher_util(self):
        """ Search by black """
        self.set_black_lines([1,0,0,0,0])
        self.set_white_lines([2,0,0,0,0])

        self.set_turn_player_colour(BLACK)
        u_with_move = self.s.utility()

        self.set_turn_player_colour(WHITE)
        self.set_search_player_colour(BLACK)
        u_not_to_move = self.s.utility()

        self.assertGreater(u_with_move, u_not_to_move)

    def test_next_to_middle_is_better(self):
        """ Search by white """
        self.set_turn_player_colour(BLACK)
        self.set_search_player_colour(WHITE)

        # (-783, [16, 0, 0, 0, 0][11, 0, 0, 0, 0] - (3, 3) next to 4,4
        self.set_black_lines([16,0,0,0,0])
        self.set_white_lines([11,0,0,0,0])
        u_adjacent = self.s.utility()

        # (-588, [17, 0, 0, 0, 0][7, 0, 0, 0, 0] - (6, 6) with a gap
        self.set_black_lines([17,0,0,0,0])
        self.set_white_lines([7,0,0,0,0])
        u_dist = self.s.utility()

        self.assertGreater(u_adjacent, u_dist)

    ##############

    def test_one_take_is_worth_more_than_a_few_pairs(self):
        self.set_search_player_colour(BLACK)
        self.set_turn_player_colour(BLACK)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([11,3,0,0,0])
        self.s.takes = [0, 1, 0]
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_one_take_is_worth_less_than_two_threes(self):
        self.set_search_player_colour(BLACK)
        self.set_turn_player_colour(BLACK)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,2,0,0])
        self.s.takes = [0, 1, 0]
        u = self.s.utility()
        self.assertLess(u, 0)

    def test_one_take_with_the_move_is_worth_more_than_one_three(self):
        self.set_search_player_colour(BLACK)
        self.set_turn_player_colour(BLACK)

        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.s.takes = [0, 1, 0]
        u = self.s.utility()
        self.assertGreater(u, 0)

    def test_one_three_with_the_move_is_worth_more_than_one_take(self):
        self.set_search_player_colour(BLACK)
        self.set_turn_player_colour(WHITE)

        #pdb.set_trace()
        self.set_black_lines([0,0,0,0,0])
        self.set_white_lines([0,0,1,0,0])
        self.s.takes = [0, 1, 0]
        u = self.s.utility()
        self.assertLess(u, 0)


if __name__ == "__main__":
    unittest.main()



