#!/usr/bin/env python

import unittest

from game_state import *
from player import *
from rules import *
from game import *

B = BLACK
W = WHITE

class GameStateTest(unittest.TestCase):
    def setUp(self):
        self.setUpWithOverrides(
                size=5,
                player1=HumanPlayer("Fred"),
                player2=HumanPlayer("Wilma"))

    def setUpWithOverrides(self, size=5, player1=None, player2=None, rules_str="standard"):
        rules = Rules(size, rules_str)
        self.game = Game(rules, player1, player2)
        self.gs = GameState(self.game)

    def move(self, x, y):
        self.gs.make_move(Move(Pos(x,y)))

    def aE(self, a, b):
        self.assertEquals(a, b)

    def test_create_game_state_move_one(self):
        self.aE(self.gs.get_move_number(), 1)
        self.aE(self.gs.get_captured(B), 0)
        self.aE(self.gs.get_captured(W), 0)

    def test_make_one_move(self):
        self.move(2,4)
        self.aE(self.gs.get_move_number(), 2)
        self.aE(self.gs.get_captured(B), 0)
        self.aE(self.gs.get_captured(W), 0)

    def test_make_one_N_capture(self):
        self.move(2,4)
        self.move(1,4)
        self.move(3,4)
        self.move(4,4)
        self.aE(self.gs.get_move_number(), 5)
        self.aE(self.gs.get_captured(EMPTY), 0)
        self.aE(self.gs.get_captured(B), 0)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_NE_capture(self):
        self.move(2,2)
        self.move(1,1)
        self.move(3,3)
        self.move(4,4)
        self.aE(self.gs.get_move_number(), 5)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_E_capture(self):
        self.move(2,1)
        self.move(1,1)
        self.move(3,1)
        self.move(4,1)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_SE_capture(self):
        self.move(2,3)
        self.move(1,4)
        self.move(3,2)
        self.move(4,1)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_S_capture(self):
        self.move(1,3)
        self.move(1,4)
        self.move(1,2)
        self.move(1,1)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_SW_capture(self):
        self.move(3,3)
        self.move(4,4)
        self.move(2,2)
        self.move(1,1)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_W_capture(self):
        self.move(3,1)
        self.move(4,1)
        self.move(2,1)
        self.move(1,1)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_NW_capture(self):
        self.move(3,2)
        self.move(4,1)
        self.move(2,3)
        self.move(1,4)
        self.aE(self.gs.get_captured(W), 2)

    def test_make_one_black_capture(self):
        self.move(3,2) # B
        self.move(3,1) # W
        self.move(4,1) # B
        self.move(2,1) # W
        self.move(1,1) # B
        self.aE(self.gs.get_captured(B), 2)

if __name__ == "__main__":
    unittest.main()



