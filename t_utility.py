#!/usr/bin/env python

import unittest

from length_counter import *
from ab_bridge import *
from player import *
import game_state
from board import *
from mock import *

import pdb

class UtilityTest(unittest.TestCase):
    def setUp(self):
        self.s = ABState()
        self.captured = [0, 0, 0]
        gs = Mock( {"add_observer": None, "get_all_captured": self.captured})
        gs.board = Board(13)
        self.s.set_state(gs)
        self.black_player = Player("Whatever", BLACK)

    def set_captured(self, black_captures, white_captures):
        self.captured[BLACK] = black_captures
        self.captured[WHITE] = white_captures

    def test_utility_single_stone_better_than_none(self):
        self.s.black_lines = LengthCounter([20,0,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertGreater(u, 0)

    def test_utility_more_singles_is_better(self):
        self.s.black_lines = LengthCounter([1,0,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertGreater(u, 0)

    def test_utility_more_twos_is_better(self):
        self.s.black_lines = LengthCounter([0,1,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertGreater(u, 0)

    def test_utility_more_threes_is_better(self):
        self.s.black_lines = LengthCounter([0,0,1,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertGreater(u, 0)

    def test_utility_more_fours_is_better(self):
        self.s.black_lines = LengthCounter([0,0,0,1,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertGreater(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.s.black_lines = LengthCounter([0,0,0,0,0])
        self.s.white_lines = LengthCounter([1,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertLess(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.s.black_lines = LengthCounter([0,0,0,0,0])
        self.s.white_lines = LengthCounter([1,0,0,0,0])
        u = self.s.utility(self.black_player)
        self.assertLess(u, 0)

    def test_utility_five_is_a_win(self):
        self.s.black_lines = LengthCounter([0,0,0,0,1])
        self.s.white_lines = LengthCounter([99,99,99,99,0])
        u = self.s.utility(self.black_player)
        self.assertGreaterEqual(u, alpha_beta.infinity)

    def test_black_win_by_captures(self):
        pdb.set_trace()
        self.s.black_lines = LengthCounter([0,0,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        self.set_captured(10, 0)
        u = self.s.utility(self.black_player)
        self.assertGreaterEqual(u, alpha_beta.infinity)

if __name__ == "__main__":
    unittest.main()



