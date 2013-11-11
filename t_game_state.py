#!/usr/bin/env python

import unittest

from game_state import *
from human_player import *
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
        self.gs = self.game.current_state

    def move(self, x, y, finished_check=None):
        self.gs.make_move(Pos(x,y))
        if finished_check != None:
            self.assertEquals(self.game.finished(), finished_check)

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

    def test_make_one_move(self):
        self.move(2,4)
        try:
            self.move(2,4)
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is already occupied")
            return
        self.fail()

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

    def test_unfinished(self):
        self.aE(self.game.finished(), False)
        self.aE(self.gs.get_won_by(), EMPTY)

    ###########################################
    # 5 in a row should win
    ###########################################

    def test_N_5_in_a_row_detected(self):
        self.aE(self.game.finished(), False)
        self.move(1,1,False) # B
        self.move(3,1,False) # W
        self.move(1,2,False) # B
        self.move(2,1,False) # W
        self.move(1,3,False) # B
        self.move(5,4,False) # W
        self.move(1,4,False) # B
        self.move(2,4,False) # W
        self.move(1,5,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_NE_5_in_a_row_detected(self):
        self.move(1,1,False) # B
        self.move(3,1,False) # W
        self.move(2,2,False) # B
        self.move(2,1,False) # W
        self.move(3,3,False) # B
        self.move(5,4,False) # W
        self.move(4,4,False) # B
        self.move(2,4,False) # W
        self.move(5,5,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_E_5_in_a_row_detected(self):
        self.move(1,1,False) # B
        self.move(3,2,False) # W
        self.move(2,1,False) # B
        self.move(2,3,False) # W
        self.move(3,1,False) # B
        self.move(5,4,False) # W
        self.move(4,1,False) # B
        self.move(2,4,False) # W
        self.move(5,1,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_SE_5_in_a_row_detected(self):
        self.move(1,5,False) # B
        self.move(3,2,False) # W
        self.move(2,4,False) # B
        self.move(2,3,False) # W
        self.move(3,3,False) # B
        self.move(5,4,False) # W
        self.move(4,2,False) # B
        self.move(2,5,False) # W
        self.move(5,1,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_S_5_in_a_row_detected(self):
        self.move(1,5,False) # B
        self.move(3,2,False) # W
        self.move(1,4,False) # B
        self.move(2,3,False) # W
        self.move(1,3,False) # B
        self.move(5,4,False) # W
        self.move(1,2,False) # B
        self.move(2,5,False) # W
        self.move(1,1,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_SW_5_in_a_row_detected(self):
        self.move(5,5,False) # B
        self.move(3,2,False) # W
        self.move(4,4,False) # B
        self.move(2,3,False) # W
        self.move(3,3,False) # B
        self.move(5,4,False) # W
        self.move(2,2,False) # B
        self.move(2,5,False) # W
        self.move(1,1,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_W_5_in_a_row_detected(self):
        self.move(5,1,False) # B
        self.move(3,2,False) # W
        self.move(4,1,False) # B
        self.move(2,3,False) # W
        self.move(3,1,False) # B
        self.move(5,4,False) # W
        self.move(2,1,False) # B
        self.move(2,5,False) # W
        self.move(1,1,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_NW_5_in_a_row_detected(self):
        self.move(5,1,False) # B
        self.move(3,2,False) # W
        self.move(4,2,False) # B
        self.move(2,3,False) # W
        self.move(3,3,False) # B
        self.move(5,4,False) # W
        self.move(2,4,False) # B
        self.move(2,5,False) # W
        self.move(1,5,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_for_5_captures(self):
        self.setUpWithOverrides(size=13)

        # First halves
        self.move(1,1,False) # B
        self.move(2,1,False) # W
        self.move(1,2,False) # B
        self.move(2,2,False) # W
        self.move(1,3,False) # B
        self.move(2,3,False) # W
        self.move(1,5,False) # B # NB don't make a line of 5
        self.move(2,5,False) # W
        self.move(1,6,False) # B
        self.move(2,6,False) # W

        # Switch to white first
        self.move(5,5,False) # B
        
        # capture 5 pairs
        self.move(3,1,False) # W
        self.move(4,1,False) # B
        self.move(3,2,False) # W
        self.move(4,2,False) # B
        self.move(3,3,False) # W
        self.move(4,3,False) # B
        self.move(3,5,False) # W
        self.move(4,5,False) # B
        self.move(3,6,False) # W
        self.move(4,6,True) # B # finished game
        self.aE(self.gs.captured[1], 10)
        self.aE(self.gs.get_won_by(), B)

if __name__ == "__main__":
    unittest.main()

