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
        self.assertEqual(x, 5)
        self.assertEqual(y, 5)
        self.assertEqual(brd.get_occ((5,5)), BLACK)

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
        self.assertEqual(x, 2)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((5,5)), BLACK)

    def test_only_shift_y(self):
        self.game.load_moves("1. (5, 7)\n")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 2)
        self.assertEqual(brd.get_occ((5,5)), BLACK)

    def test_only_shift_y_because_of_right_edge(self):
        self.game.load_moves("1. (7, 7)\n2. (14, 7)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 2)
        self.assertEqual(brd.get_occ((7,5)), BLACK)
        self.assertEqual(brd.get_occ((14,5)), WHITE)

    def test_only_shift_x_because_of_top_edge(self):
        self.game.load_moves("1. (7, 7)\n2. (7, 14)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 2)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((5,7)), BLACK)
        self.assertEqual(brd.get_occ((5,14)), WHITE)

    def test_shift_a_few_both_ways(self):
        self.game.load_moves("1. (8, 7)\n2. (8, 10)\n3. (9, 11)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 3)
        self.assertEqual(y, 2)
        self.assertEqual(brd.get_occ((5,5)), BLACK)
        self.assertEqual(brd.get_occ((5,8)), WHITE)
        self.assertEqual(brd.get_occ((6,9)), BLACK)

    def test_shift_left_in_spite_of_right_edge(self):
        self.game.load_moves("1. (7, 5)\n2. (13, 5)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 2)
        self.assertEqual(y, 0)
        self.assertEqual(brd.get_occ((5,5)), BLACK)
        self.assertEqual(brd.get_occ((11,5)), WHITE)

    def test_shift_down_in_spite_of_top_edge(self):
        self.game.load_moves("1. (5, 9)\n2. (5, 13)")
        std, x, y = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(x, 0)
        self.assertEqual(y, 4)
        self.assertEqual(brd.get_occ((5,5)), BLACK)
        self.assertEqual(brd.get_occ((5,9)), WHITE)

    ################################################################
    # Corner tests

    # !python pentai/ai/t_trans_standardise.py TransStandardiseTest.test_NE
    def test_corners(self):
        for pos in [(0,18), (18,18), (18,0), (0,0)]:
            self.game.load_moves("1. %s" % (pos,))
            std, l_shift, d_shift = shift(self.game.current_state)

            brd = std.get_board()
            self.assertEqual(l_shift, 0)
            self.assertEqual(d_shift, 0)

    # !python pentai/ai/t_trans_standardise.py TransStandardiseTest.test_outer_edges1
    def test_outer_edges1(self):
        self.outer_edge_check((4,14))
        
    def test_outer_edges2(self):
        self.outer_edge_check((14,14))
        
    def test_outer_edges3(self):
        self.outer_edge_check((14,4))
        
    def test_outer_edges4(self):
        self.outer_edge_check((4,4))
        
    def outer_edge_check(self, pos):
        # These should stay where they are because they are close to
        # an edge.
        self.game.load_moves("1. %s" % (pos,))
        std, l_shift, d_shift = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(l_shift, 0)
        self.assertEqual(d_shift, 0)

    # !python pentai/ai/t_trans_standardise.py TransStandardiseTest.test_inner_edges
    def test_inner_edges1(self):
        self.inner_edge_check((5,12))

    def test_inner_edges2(self):
        self.inner_edge_check((6,12))

    def test_inner_edges3(self):
        self.inner_edge_check((12,12))
        
    def test_inner_edges4(self):
        self.inner_edge_check((12,5))

    def test_inner_edges5(self):
        self.inner_edge_check((5,5))

    def inner_edge_check(self, pos):
        # These should all move to (5,5)
        self.game.load_moves("1. %s" % (pos,))
        std, l_shift, d_shift = shift(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(l_shift, pos[0] - 5)
        self.assertEqual(d_shift, pos[1] - 5)


if __name__ == "__main__":
    unittest.main()
