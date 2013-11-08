#!/usr/bin/env python

import unittest

from length_counter import *
from utility import *

import pdb

class UtilityTest(unittest.TestCase):

    def test_utility_single_stone_better_than_none(self):
        black_lengths = LengthCounter([20,0,0,0,0])
        white_lengths = LengthCounter([0,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreater(u, 0)

    def test_utility_more_singles_is_better(self):
        black_lengths = LengthCounter([1,0,0,0,0])
        white_lengths = LengthCounter([0,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreater(u, 0)

    def test_utility_more_twos_is_better(self):
        black_lengths = LengthCounter([0,1,0,0,0])
        white_lengths = LengthCounter([0,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreater(u, 0)

    def test_utility_more_threes_is_better(self):
        black_lengths = LengthCounter([0,0,1,0,0])
        white_lengths = LengthCounter([0,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreater(u, 0)

    def test_utility_more_fours_is_better(self):
        black_lengths = LengthCounter([0,0,0,1,0])
        white_lengths = LengthCounter([0,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreater(u, 0)

    def test_utility_less_ones_is_worse(self):
        black_lengths = LengthCounter([0,0,0,0,0])
        white_lengths = LengthCounter([1,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertLess(u, 0)

    def test_utility_less_ones_is_worse(self):
        black_lengths = LengthCounter([0,0,0,0,0])
        white_lengths = LengthCounter([1,0,0,0,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertLess(u, 0)

    def test_utility_five_is_a_win(self):
        black_lengths = LengthCounter([0,0,0,0,1])
        white_lengths = LengthCounter([99,99,99,99,0])
        captures = [0,0]
        u = utility(black_lengths, white_lengths, captures)
        self.assertGreaterEqual(u, infinity)

if __name__ == "__main__":
    unittest.main()



