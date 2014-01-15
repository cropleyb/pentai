#!/usr/bin/env python

import unittest
from openings_filter import *
from board import *

import pdb

class MockGame:
    def __init__(self, wc):
        self.winner_colour = wc

    def winner(self):
        return self.winner_colour

class OpeningsFilterTest(unittest.TestCase):
    def setUp(self):
        self.of = OpeningsFilter()

    def test_no_moves_available_suggest_nothing(self):
        move_games = []
        self.of.set_move_games(move_games)
        move = self.of.get_a_good_move(BLACK)
        self.assertEquals(move, None)

    def test_one_favourable_game(self):
        g1 = MockGame(BLACK)
        move_games = [((4,4), (g1,))]
        self.of.set_move_games(move_games)
        move = self.of.get_a_good_move(BLACK)
        self.assertEquals(move, (4,4))

if __name__ == "__main__":
    unittest.main()

