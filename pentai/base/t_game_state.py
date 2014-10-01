#!/usr/bin/env python

import unittest

from pentai.base.pente_exceptions import IllegalMoveException
from pentai.base.game_state import *
from pentai.base.human_player import *
from pentai.base.rules import *
from pentai.base.game import *

from pentai.base.mock import *

B = P1
W = P2

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
        self.gs.make_move((x,y))
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

    def test_make_one_move_clash(self):
        self.move(2,4)
        try:
            self.move(2,4)
        except IllegalMoveException, e:
            self.assertEquals(e.message, "Position C4 is already occupied")
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
        self.move(0,0,False) # B
        self.move(2,0,False) # W
        self.move(0,1,False) # B
        self.move(1,0,False) # W
        self.move(0,2,False) # B
        self.move(4,3,False) # W
        self.move(0,3,False) # B
        self.move(1,3,False) # W
        self.move(0,4,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_NE_5_in_a_row_detected(self):
        self.move(0,0,False) # B
        self.move(2,0,False) # W
        self.move(1,1,False) # B
        self.move(1,0,False) # W
        self.move(2,2,False) # B
        self.move(4,3,False) # W
        self.move(3,3,False) # B
        self.move(1,3,False) # W
        self.move(4,4,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_E_5_in_a_row_detected(self):
        self.move(0,0,False) # B
        self.move(2,1,False) # W
        self.move(1,0,False) # B
        self.move(1,2,False) # W
        self.move(2,0,False) # B
        self.move(4,3,False) # W
        self.move(3,0,False) # B
        self.move(1,3,False) # W
        self.move(4,0,True) # B
        self.aE(self.gs.get_won_by(), B)

    # !./pentai/base/t_game_state.py GameStateTest.test_SE_5_in_a_row_detected
    def test_SE_5_in_a_row_detected(self):
        self.setUpWithOverrides(
                size=19,
                player1=HumanPlayer("Me"),
                player2=HumanPlayer("Myself"))
        self.move(14,14,False) # B
        self.move(16,17,False) # W
        self.move(15,15,False) # B
        self.move(15,16,False) # W
        self.move(16,16,False) # B
        self.move(18,15,False) # W
        self.move(17,17,False) # B
        self.move(15,14,False) # W
        self.move(18,18,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_S_5_in_a_row_detected(self):
        self.move(0,4,False) # B
        self.move(2,1,False) # W
        self.move(0,3,False) # B
        self.move(1,2,False) # W
        self.move(0,2,False) # B
        self.move(4,3,False) # W
        self.move(0,1,False) # B
        self.move(1,4,False) # W
        self.move(0,0,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_SW_5_in_a_row_detected(self):
        self.move(4,4,False) # B
        self.move(2,1,False) # W
        self.move(3,3,False) # B
        self.move(1,2,False) # W
        self.move(2,2,False) # B
        self.move(4,3,False) # W
        self.move(1,1,False) # B
        self.move(1,4,False) # W
        self.move(0,0,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_W_5_in_a_row_detected(self):
        self.move(4,0,False) # B
        self.move(2,1,False) # W
        self.move(3,0,False) # B
        self.move(1,2,False) # W
        self.move(2,0,False) # B
        self.move(4,3,False) # W
        self.move(1,0,False) # B
        self.move(1,4,False) # W
        self.move(0,0,True) # B
        self.aE(self.gs.get_won_by(), B)

    def test_NW_5_in_a_row_detected(self):
        self.move(4,0,False) # B
        self.move(2,1,False) # W
        self.move(3,1,False) # B
        self.move(1,2,False) # W
        self.move(2,2,False) # B
        self.move(4,3,False) # W
        self.move(1,3,False) # B
        self.move(1,4,False) # W
        self.move(0,4,True) # B
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

# TODO Undo Copy and paste
class ObserverTest(unittest.TestCase):
    def setUp(self):
        self.setUpWithOverrides(
                size=5,
                player1=HumanPlayer("Fred"),
                player2=HumanPlayer("Wilma"))

    def setUpWithOverrides(self, size=5, player1=None, player2=None, rules_str="standard"):
        rules = Rules(size, rules_str)
        self.game = Game(rules, player1, player2)
        self.gs = self.game.current_state

    def move(self, x, y):
        self.gs.make_move((x,y))

    def test_capture_is_observed(self):
        m = Mock()
        self.gs.add_observer(m)
        self.move(3,1) # B
        self.move(4,1) # W
        self.move(2,1) # B
        self.move(1,1) # W

        all_calls = m.mockGetAllCalls()
        # Before and after inc. two captures
        self.assertEquals(len(all_calls), 12)
        
    def test_set_won_by_observed(self):
        m = Mock()
        self.gs.add_observer(m)
        self.gs.set_won_by(P2)

        all_calls = m.mockGetAllCalls()
        self.assertEquals(len(all_calls), 1)
        m.mockCheckCall(0, 'after_game_won', self.game, P2)


if __name__ == "__main__":
    unittest.main()

