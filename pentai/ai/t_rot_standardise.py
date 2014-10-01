#!/usr/bin/env python

import unittest

from pentai.base.game_state import *
from pentai.base.game import *
import pentai.base.player as p_m
from pentai.base.rules import *
from pentai.ai.rot_standardise import *

class RotStandardiseTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(9, "standard")
        self.game = Game(self.rules, p_m.Player("BC"), p_m.Player("Whoever"))

    ###################################################
    # flip tests

    def test_page_flip(self): # TODO: rename to flip
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gpf = page_flip(self.game.current_state)
        brd = gpf.get_board()

        self.assertEqual(brd.get_occ((8,0)), P1)
        self.assertEqual(brd.get_occ((5,3)), P2)
        self.assertEqual(brd.get_occ((5,4)), P1)
        self.assertEqual(brd.get_occ((3,4)), P2)

    def test_calendar_flip(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gcf = calendar_flip(self.game.current_state)
        brd = gcf.get_board()

        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((3,5)), P2)
        self.assertEqual(brd.get_occ((3,4)), P1)
        self.assertEqual(brd.get_occ((5,4)), P2)

    def test_diagonal_flip(self):
        """ i.e. swap x and y """
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        brd = gdf.get_board()

        self.assertEqual(brd.get_occ((0,0)), P1)
        self.assertEqual(brd.get_occ((3,3)), P2)
        self.assertEqual(brd.get_occ((4,3)), P1)
        self.assertEqual(brd.get_occ((4,5)), P2)

    def test_diagonal_then_page(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        gpf = page_flip(self.game.current_state)
        brd = gpf.get_board()

        self.assertEqual(brd.get_occ((8,0)), P1)
        self.assertEqual(brd.get_occ((5,3)), P2)
        self.assertEqual(brd.get_occ((4,3)), P1)
        self.assertEqual(brd.get_occ((4,5)), P2)

    def test_diagonal_then_calendar(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        gcf = calendar_flip(self.game.current_state)
        brd = gcf.get_board()

        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((3,5)), P2)
        self.assertEqual(brd.get_occ((4,5)), P1)
        self.assertEqual(brd.get_occ((4,3)), P2)

    ###################################################
    # standardise position tests for 9x9
    def test_standardise_SW_corner_pos(self):
        self.game.load_moves("1. (0,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)

    def test_standardise_NW_corner_pos(self):
        self.game.load_moves("1. (0,8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)

    def test_standardise_NE_corner_pos(self):
        self.game.load_moves("1. (8,8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)

    def test_standardise_SE_corner_pos(self):
        self.game.load_moves("1. (8,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)

    ###################################################
    # standardise position tests with two pieces

    def test_standardise_SW_W(self):
        self.game.load_moves("1. (0,0)\n2. (0, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    def test_standardise_SW_S(self):
        self.game.load_moves("1. (0,0)\n2. (4, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    # !./t_standardise.py RotStandardiseTest.test_standardise_NW_W
    def test_standardise_NW_W(self):
        self.game.load_moves("1. (0,8)\n2. (0, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    # !./t_standardise.py RotStandardiseTest.test_standardise_NW_N
    def test_standardise_NW_N(self):
        self.game.load_moves("1. (0,8)\n2. (4, 8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    def test_standardise_NE_E(self):
        self.game.load_moves("1. (8,8)\n2. (8, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    def test_standardise_NE_N(self):
        self.game.load_moves("1. (8, 8)\n2. (4, 8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    def test_standardise_SE_E(self):
        self.game.load_moves("1. (8, 0)\n2. (8, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

    def test_standardise_SE_S(self):
        self.game.load_moves("1. (8, 0)\n2. (4, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), P1)
        self.assertEqual(brd.get_occ((4,8)), P2)

class RotStandardisePositionTest(unittest.TestCase):
    ###################################################
    # standardise position tests
    def setUp(self):
        self.rules = Rules(19, "standard")
        self.game = Game(self.rules, p_m.Player("BC"), p_m.Player("Whoever"))

    def test_standardise_SW_corner_pos(self):
        self.game.load_moves("1. (0,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)

    def test_standardise_NW_corner_pos(self):
        self.game.load_moves("1. (0,18)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)

    def test_standardise_NE_corner_pos(self):
        self.game.load_moves("1. (18,18)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)

    def test_standardise_SE_corner_pos(self):
        self.game.load_moves("1. (18,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)

    ###################################################
    # standardise position tests with two pieces

    def test_standardise_SW_W(self):
        self.game.load_moves("1. (0,0)\n2. (0, 9)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    def test_standardise_SW_S(self):
        self.game.load_moves("1. (0,0)\n2. (9, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    # !./t_standardise.py RotStandardiseTest.test_standardise_NW_W
    def test_standardise_NW_W(self):
        self.game.load_moves("1. (0,18)\n2. (0, 9)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    # !./t_standardise.py RotStandardiseTest.test_standardise_NW_N
    def test_standardise_NW_N(self):
        self.game.load_moves("1. (0,18)\n2. (9, 18)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        #print brd
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    def test_standardise_NE_E(self):
        self.game.load_moves("1. (18,18)\n2. (18, 9)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    def test_standardise_NE_N(self):
        self.game.load_moves("1. (18, 18)\n2. (9, 18)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    def test_standardise_SE_E(self):
        self.game.load_moves("1. (18, 0)\n2. (18, 9)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

    def test_standardise_SE_S(self):
        self.game.load_moves("1. (18, 0)\n2. (9, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,18)), P1)
        self.assertEqual(brd.get_occ((9,18)), P2)

if __name__ == "__main__":
    unittest.main()
