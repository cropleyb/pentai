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

    def test_create_game_state_move_one(self):
        gs = GameState(self.game)
        self.assertEquals(gs.get_move_number(), 1)
        self.assertEquals(gs.get_captured(B), 0)
        self.assertEquals(gs.get_captured(W), 0)

    def test_make_one_move(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,4)))
        self.assertEquals(gs.get_move_number(), 2)
        self.assertEquals(gs.get_captured(B), 0)
        self.assertEquals(gs.get_captured(W), 0)

    def test_make_one_N_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,4)))
        gs.make_move(Move(Pos(1,4)))
        gs.make_move(Move(Pos(3,4)))
        gs.make_move(Move(Pos(4,4)))
        self.assertEquals(gs.get_move_number(), 5)
        self.assertEquals(gs.get_captured(EMPTY), 0)
        self.assertEquals(gs.get_captured(B), 0)
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_NE_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,2)))
        gs.make_move(Move(Pos(1,1)))
        gs.make_move(Move(Pos(3,3)))
        gs.make_move(Move(Pos(4,4)))
        self.assertEquals(gs.get_move_number(), 5)
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_E_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,1)))
        gs.make_move(Move(Pos(1,1)))
        gs.make_move(Move(Pos(3,1)))
        gs.make_move(Move(Pos(4,1)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_SE_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,3)))
        gs.make_move(Move(Pos(1,4)))
        gs.make_move(Move(Pos(3,2)))
        gs.make_move(Move(Pos(4,1)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_S_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(1,3)))
        gs.make_move(Move(Pos(1,4)))
        gs.make_move(Move(Pos(1,2)))
        gs.make_move(Move(Pos(1,1)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_SW_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(3,3)))
        gs.make_move(Move(Pos(4,4)))
        gs.make_move(Move(Pos(2,2)))
        gs.make_move(Move(Pos(1,1)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_W_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(3,1)))
        gs.make_move(Move(Pos(4,1)))
        gs.make_move(Move(Pos(2,1)))
        gs.make_move(Move(Pos(1,1)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_NW_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(3,2)))
        gs.make_move(Move(Pos(4,1)))
        gs.make_move(Move(Pos(2,3)))
        gs.make_move(Move(Pos(1,4)))
        self.assertEquals(gs.get_captured(W), 2)

    def test_make_one_black_capture(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(3,2))) # B
        gs.make_move(Move(Pos(3,1))) # W
        gs.make_move(Move(Pos(4,1))) # B
        gs.make_move(Move(Pos(2,1))) # W
        gs.make_move(Move(Pos(1,1))) # B
        self.assertEquals(gs.get_captured(B), 2)

if __name__ == "__main__":
    unittest.main()



