#!/usr/bin/env python

import unittest

from pentai.base.game_state import *
from pentai.base.game import *
from pentai.base.rules import *
from pentai.ai.trans_standardise import *

class TransStandardiseTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "5")
        self.game = Game(self.rules, p_m.Player("BC"), p_m.Player("Whoever"))

    def test_shift_left_and_down(self):
        self.game.load_moves("1. (10, 10)\n")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 4)
        self.assertEqual(y, 4)
        self.assertEqual(brd.get_occ((6,6)), BLACK)

    def test_dont_shift(self):
        self.game.load_moves("1. (5, 5)\n")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((5,5)), BLACK)

    def test_only_shift_x(self):
        self.game.load_moves("1. (7, 5)\n")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((6,5)), BLACK)

    def test_only_shift_y(self):
        self.game.load_moves("1. (5, 7)\n")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        self.assertEqual(brd.get_occ((5,6)), BLACK)

    def test_only_shift_y_because_of_right_edge(self):
        self.game.load_moves("1. (7, 7)\n2. (15, 7)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        self.assertEqual(brd.get_occ((7,6)), BLACK)
        self.assertEqual(brd.get_occ((15,6)), WHITE)

    def test_only_shift_x_because_of_top_edge(self):
        self.game.load_moves("1. (7, 7)\n2. (7, 15)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((6,7)), BLACK)
        self.assertEqual(brd.get_occ((6,15)), WHITE)

    def test_shift_a_few_both_ways(self):
        self.game.load_moves("1. (8, 7)\n2. (8, 10)\n3. (9, 11)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 2)
        self.assertEqual(y, 1)
        self.assertEqual(brd.get_occ((6,6)), BLACK)
        self.assertEqual(brd.get_occ((6,9)), WHITE)
        self.assertEqual(brd.get_occ((7,10)), BLACK)

    def test_shift_left_in_spite_of_right_edge(self):
        self.game.load_moves("1. (7, 5)\n2. (14, 5)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((6,5)), BLACK)
        self.assertEqual(brd.get_occ((13,5)), WHITE)

    def test_shift_down_in_spite_of_top_edge(self):
        self.game.load_moves("1. (5, 9)\n2. (5, 14)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 3)
        self.assertEqual(brd.get_occ((5,6)), BLACK)
        self.assertEqual(brd.get_occ((5,11)), WHITE)

if __name__ == "__main__":
    unittest.main()
