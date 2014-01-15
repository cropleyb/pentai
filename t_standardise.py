#!/usr/bin/env python

import unittest

from game_state import *
from game import *
from openings_mgr import *
from rules import *
from standardise import *

import pdb

class StandardiseTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(9, "standard")
        self.game = Game(self.rules, Player("BC"), Player("Whoever"))

    ###################################################
    # flip tests

    def test_page_flip(self): # TODO: rename to flip
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gpf = page_flip(self.game.current_state)
        brd = gpf.get_board()

        self.assertEqual(brd.get_occ((8,0)), BLACK)
        self.assertEqual(brd.get_occ((5,3)), WHITE)
        self.assertEqual(brd.get_occ((5,4)), BLACK)
        self.assertEqual(brd.get_occ((3,4)), WHITE)

    def test_calendar_flip(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gcf = calendar_flip(self.game.current_state)
        brd = gcf.get_board()

        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((3,5)), WHITE)
        self.assertEqual(brd.get_occ((3,4)), BLACK)
        self.assertEqual(brd.get_occ((5,4)), WHITE)

    def test_diagonal_flip(self):
        """ i.e. swap x and y """
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        brd = gdf.get_board()

        self.assertEqual(brd.get_occ((0,0)), BLACK)
        self.assertEqual(brd.get_occ((3,3)), WHITE)
        self.assertEqual(brd.get_occ((4,3)), BLACK)
        self.assertEqual(brd.get_occ((4,5)), WHITE)

    def test_diagonal_flip(self):
        """ i.e. swap x and y """
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        brd = gdf.get_board()

        self.assertEqual(brd.get_occ((0,0)), BLACK)
        self.assertEqual(brd.get_occ((3,3)), WHITE)
        self.assertEqual(brd.get_occ((4,3)), BLACK)
        self.assertEqual(brd.get_occ((4,5)), WHITE)

    def test_diagonal_then_page(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        gpf = page_flip(self.game.current_state)
        brd = gpf.get_board()

        self.assertEqual(brd.get_occ((8,0)), BLACK)
        self.assertEqual(brd.get_occ((5,3)), WHITE)
        self.assertEqual(brd.get_occ((4,3)), BLACK)
        self.assertEqual(brd.get_occ((4,5)), WHITE)

    def test_diagonal_then_calendar(self):
        self.game.load_moves("1. (0,0)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        gdf = diagonal_flip(self.game.current_state)
        gcf = calendar_flip(self.game.current_state)
        brd = gcf.get_board()

        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((3,5)), WHITE)
        self.assertEqual(brd.get_occ((4,5)), BLACK)
        self.assertEqual(brd.get_occ((4,3)), WHITE)

    ###################################################
    # standardise position tests

    def test_standardise_SW_corner_pos(self):
        self.game.load_moves("1. (0,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)

    def test_standardise_NW_corner_pos(self):
        self.game.load_moves("1. (0,8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)

    def test_standardise_NE_corner_pos(self):
        self.game.load_moves("1. (8,8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)

    def test_standardise_SE_corner_pos(self):
        self.game.load_moves("1. (8,0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)

    ###################################################
    # standardise position tests with two pieces

    def test_standardise_SW_W(self):
        self.game.load_moves("1. (0,0)\n2. (0, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    def test_standardise_SW_S(self):
        self.game.load_moves("1. (0,0)\n2. (4, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    # !./t_standardise.py StandardiseTest.test_standardise_NW_W
    def test_standardise_NW_W(self):
        self.game.load_moves("1. (0,8)\n2. (0, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    # !./t_standardise.py StandardiseTest.test_standardise_NW_N
    def test_standardise_NW_N(self):
        self.game.load_moves("1. (0,8)\n2. (4, 8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        #print brd
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    def test_standardise_NE_E(self):
        self.game.load_moves("1. (8,8)\n2. (8, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    def test_standardise_NE_N(self):
        self.game.load_moves("1. (8, 8)\n2. (4, 8)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    def test_standardise_SE_E(self):
        self.game.load_moves("1. (8, 0)\n2. (8, 4)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

    def test_standardise_SE_S(self):
        self.game.load_moves("1. (8, 0)\n2. (4, 0)")
        std, fwd, rev = standardise(self.game.current_state)

        brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        self.assertEqual(brd.get_occ((0,8)), BLACK)
        self.assertEqual(brd.get_occ((4,8)), WHITE)

if __name__ == "__main__":
    unittest.main()
