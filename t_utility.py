#!/usr/bin/env python

import unittest

from length_counter import *
from ab_bridge import *
#from utility import *

class UtilityTest(unittest.TestCase):
    def setUp(self):
        self.s = ABState()

    def test_utility_single_stone_better_than_none(self):
        self.s.black_lines = LengthCounter([20,0,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(None)
        self.assertGreater(u, 0)

    def test_utility_more_singles_is_better(self):
        self.s.black_lines = LengthCounter([1,0,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(None)
        self.assertGreater(u, 0)

    def test_utility_more_twos_is_better(self):
        self.s.black_lines = LengthCounter([0,1,0,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(None)
        self.assertGreater(u, 0)

    def test_utility_more_threes_is_better(self):
        self.s.black_lines = LengthCounter([0,0,1,0,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(None)
        self.assertGreater(u, 0)

    def test_utility_more_fours_is_better(self):
        self.s.black_lines = LengthCounter([0,0,0,1,0])
        self.s.white_lines = LengthCounter([0,0,0,0,0])
        u = self.s.utility(None)
        self.assertGreater(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.s.black_lines = LengthCounter([0,0,0,0,0])
        self.s.white_lines = LengthCounter([1,0,0,0,0])
        u = self.s.utility(None)
        self.assertLess(u, 0)

    def test_utility_less_ones_is_worse(self):
        self.s.black_lines = LengthCounter([0,0,0,0,0])
        self.s.white_lines = LengthCounter([1,0,0,0,0])
        u = self.s.utility(None)
        self.assertLess(u, 0)

    def test_utility_five_is_a_win(self):
        self.s.black_lines = LengthCounter([0,0,0,0,1])
        self.s.white_lines = LengthCounter([99,99,99,99,0])
        u = self.s.utility(None)
        self.assertGreaterEqual(u, alpha_beta.infinity)

if __name__ == "__main__":
    unittest.main()



