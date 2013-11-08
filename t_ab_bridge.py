#!/usr/bin/env python

import unittest

import pdb

import alpha_beta

import game
import rules
import player
from board import *

from ab_bridge import *

class AlphaBetaBridgeTest(unittest.TestCase):

    def setUp(self):
        player1 = player.HumanPlayer("Blomp")
        player2 = player.HumanPlayer("Kubba")
        r = rules.Rules(13, "standard")
        my_game = game.Game(r, player1, player2)
        self.s = ABState()
        self.s.set_state(my_game.current_state)

    def test_update_substrips_middle_of_board(self):
        self.s.board().set_occ(Pos(7,7), BLACK)

        self.assertEquals(self.s.black_lines, [20, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_SW_corner(self):
        self.s.board().set_occ(Pos(0,0), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])
    '''
    def test_update_substrips_NE_corner(self):
        self.s.board().set_occ(Pos(13,13), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])
    '''


    def test_one_level_search(self):
        r = rules.Rules(7, "standard")
        '''
        # TODO
        alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
        # self.assertEquals() # TODO
        '''


if __name__ == "__main__":
    unittest.main()



