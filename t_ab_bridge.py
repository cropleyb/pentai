#!/usr/bin/env python

import unittest

import pdb

import alpha_beta

import game
import rules
import human_player
from board import *

from ab_bridge import *

class AlphaBetaBridgeTest(unittest.TestCase):

    def setUp(self):
        player1 = human_player.HumanPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(13, "standard")
        my_game = game.Game(r, player1, player2)
        self.s = ABState()
        self.s.set_state(my_game.current_state)

    def test_update_substrips_middle_of_board(self):
        self.s.board().set_occ(Pos(7,7), BLACK)

        self.assertEquals(self.s.black_lines, [20, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_empty_board(self):
        self.assertEquals(self.s.black_lines, [0, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_SW_corner(self):
        self.s.board().set_occ(Pos(0,0), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_near_SW_corner(self):
        self.s.board().set_occ(Pos(1,0), BLACK)

        self.assertEquals(self.s.black_lines, [4, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_NE_corner(self):
        self.s.board().set_occ(Pos(12,12), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_remove_single_stone(self):
        self.s.board().set_occ(Pos(0,0), BLACK)
        self.s.board().set_occ(Pos(0,0), EMPTY)

        self.assertEquals(self.s.black_lines, [0, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_two_blacks_SW(self):
        self.s.board().set_occ(Pos(0,0), BLACK)
        self.s.board().set_occ(Pos(1,1), BLACK)

        self.assertEquals(self.s.black_lines, [7, 1, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_2_opp_colour_pieces(self):
        self.s.board().set_occ(Pos(0,0), BLACK)
        self.s.board().set_occ(Pos(0,1), WHITE)

        self.assertEquals(self.s.black_lines, [2, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [3, 0, 0, 0, 0])

    def test_update_substrips_2_pieces(self):
        self.s.board().set_occ(Pos(0,0), BLACK)
        self.s.board().set_occ(Pos(0,1), BLACK)

        self.assertEquals(self.s.black_lines, [5, 1, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_5_in_a_row(self):
        self.s.board().set_occ(Pos(0,0), BLACK)
        self.s.board().set_occ(Pos(0,1), BLACK)
        self.s.board().set_occ(Pos(0,2), BLACK)
        self.s.board().set_occ(Pos(0,3), BLACK)
        self.s.board().set_occ(Pos(0,4), BLACK)

        self.assertEquals(self.s.black_lines, [12, 1, 1, 1, 1])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    '''
    def test_one_level_search(self):
        r = rules.Rules(7, "standard")
        
        # TODO
        alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
        # self.assertEquals() # TODO
    '''

if __name__ == "__main__":
    unittest.main()



