#!/usr/bin/env python

import unittest

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
        self.s.board().set_occ((7,7), BLACK)

        self.assertEquals(self.s.black_lines, [20, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_empty_board(self):
        self.assertEquals(self.s.black_lines, [0, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_SW_corner(self):
        self.s.board().set_occ((0,0), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_near_SW_corner(self):
        self.s.board().set_occ((1,0), BLACK)

        self.assertEquals(self.s.black_lines, [4, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_NE_corner(self):
        self.s.board().set_occ((12,12), BLACK)

        self.assertEquals(self.s.black_lines, [3, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_remove_single_stone(self):
        self.s.board().set_occ((0,0), BLACK)
        self.s.board().set_occ((0,0), EMPTY)

        self.assertEquals(self.s.black_lines, [0, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_two_blacks_SW(self):
        self.s.board().set_occ((0,0), BLACK)
        self.s.board().set_occ((1,1), BLACK)

        self.assertEquals(self.s.black_lines, [7, 1, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_2_opp_colour_pieces(self):
        self.s.board().set_occ((0,0), BLACK)
        self.s.board().set_occ((0,1), WHITE)

        self.assertEquals(self.s.black_lines, [2, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [3, 0, 0, 0, 0])

    def test_update_substrips_2_pieces(self):
        self.s.board().set_occ((0,0), BLACK)
        self.s.board().set_occ((0,1), BLACK)

        self.assertEquals(self.s.black_lines, [5, 1, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

    def test_update_substrips_5_in_a_row(self):
        self.s.board().set_occ((0,0), BLACK)
        self.s.board().set_occ((0,1), BLACK)
        self.s.board().set_occ((0,2), BLACK)
        self.s.board().set_occ((0,3), BLACK)
        self.s.board().set_occ((0,4), BLACK)

        self.assertEquals(self.s.black_lines, [12, 1, 1, 1, 1])
        self.assertEquals(self.s.white_lines, [0, 0, 0, 0, 0])

class LengthCounterTest(unittest.TestCase):

    def setUp(self):
        player1 = human_player.HumanPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(9, "standard")
        my_game = game.Game(r, player1, player2)
        self.s = ABState()
        self.s.set_state(my_game.current_state)

    def test_middle_for_black_diag_2_for_white(self):
        self.s.board().set_occ((4,4), BLACK)
        self.s.board().set_occ((2,2), WHITE)

        self.assertEquals(self.s.black_lines, [17, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [7, 0, 0, 0, 0])
        
    def test_middle_for_black_left_1_for_white(self):
        self.s.board().set_occ((4,4), BLACK)
        self.s.board().set_occ((3,4), WHITE)

        self.assertEquals(self.s.black_lines, [16, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [5+4+4, 0, 0, 0, 0])

    def test_middle_for_black_right_1_for_white(self):
        self.s.board().set_occ((4,4), BLACK)
        self.s.board().set_occ((5,4), WHITE)

        self.assertEquals(self.s.black_lines, [16, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [5+4+4, 0, 0, 0, 0])

    def test_middle_for_black_up_1_for_white(self):
        self.s.board().set_occ((4,4), BLACK)
        self.s.board().set_occ((4,5), WHITE)

        self.assertEquals(self.s.black_lines, [16, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [5+4+4, 0, 0, 0, 0])

    def test_middle_for_black_down_1_for_white(self):
        self.s.board().set_occ((4,4), BLACK)
        self.s.board().set_occ((4,3), WHITE)

        self.assertEquals(self.s.black_lines, [16, 0, 0, 0, 0])
        self.assertEquals(self.s.white_lines, [5+4+4, 0, 0, 0, 0])

    ###############

class MoreAlphaBetaBridgeTests(unittest.TestCase):
    def setUp(self):
        player1 = human_player.HumanPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(5, "standard")
        my_game = game.Game(r, player1, player2)
        self.s = ABState()
        self.s.set_state(my_game.current_state)

    def test_initial_state_black_to_move(self):
        self.assertEquals(self.s.to_move_colour(), BLACK)

    def test_create_state(self):
        child = self.s.create_state((2,2))
        self.assertEquals(child.to_move_colour(), WHITE)
        self.assertEquals(child.terminal(), False)
        board = child.board()
        self.assertEquals(board.get_occ((2,2)), BLACK)
        self.assertEquals(board.get_occ((3,3)), EMPTY)
        self.assertEquals(board.get_occ((1,1)), EMPTY)

    def test_length_counters_after_sw_corner(self):
        g1 = self.s.create_state((0,0)) # B
        self.assertEquals(g1.get_black_line_counts().tup(), (3, 0, 0, 0, 0))

    def test_length_counters_after_nw_corner(self):
        g1 = self.s.create_state((0,4)) # B
        self.assertEquals(g1.get_black_line_counts().tup(), (3, 0, 0, 0, 0))

    def test_length_counters_after_ne_corner(self):
        g1 = self.s.create_state((4,4)) # B
        self.assertEquals(g1.get_black_line_counts().tup(), (3, 0, 0, 0, 0))

    def test_length_counters_after_se_corner(self):
        g1 = self.s.create_state((4,0)) # B
        self.assertEquals(g1.get_black_line_counts().tup(), (3, 0, 0, 0, 0))

    def test_cannot_place_off_e_edge(self):
        try:
            g1 = self.s.create_state((-1,2)) # B
        except game.IllegalMoveException:
            return
        self.assertFail()
    
    def test_length_counters_after_two_moves(self):
        g1 = self.s.create_state((0,0)) # B
        g2 =     g1.create_state((1,1)) # W
        self.assertEquals(g2.get_black_line_counts().tup(), (2, 0, 0, 0, 0))
        self.assertEquals(g2.get_white_line_counts().tup(), (2, 0, 0, 0, 0))

    def test_length_counters_after_two_moves_b(self):
        g1 = self.s.create_state((1,1)) # B
        g2 =     g1.create_state((2,2)) # W
        self.assertEquals(g2.get_black_line_counts().tup(), (2, 0, 0, 0, 0))
        # One across the other diagonal
        self.assertEquals(g2.get_white_line_counts().tup(), (3, 0, 0, 0, 0))

    def test_length_counters_after_five_moves(self):
        # along the NE diagonal
        g1 = self.s.create_state((1,1)) # B
        g2 =     g1.create_state((2,2)) # W
        g3 =     g2.create_state((3,3)) # B
        g4 =     g3.create_state((4,4)) # W
        g5 =     g4.create_state((0,0)) # B
        self.assertEquals(g5.get_black_line_counts().tup(), (6, 0, 0, 0, 0))
        self.assertEquals(g5.get_white_line_counts().tup(), (5, 0, 0, 0, 0))

    def test_length_counters_after_five_moves_in_cnrs_and_middle(self):
        # four in the corners and one in the middle
        g1 = self.s.create_state((0,0)) # B
        g2 =     g1.create_state((0,4)) # W
        g3 =     g2.create_state((4,4)) # B
        g4 =     g3.create_state((4,0)) # W
        g5 =     g4.create_state((2,2)) # B
        self.assertEquals(g5.get_black_line_counts().tup(), (2, 0, 1, 0, 0))
        self.assertEquals(g5.get_white_line_counts().tup(), (0, 0, 0, 0, 0))

    def test_make_a_capture(self):
        g1 = self.s.create_state((0,1)) # B
        g2 =     g1.create_state((1,2)) # W
        g3 =     g2.create_state((1,3)) # B
        g4 =     g3.create_state((2,3)) # W
        g5 =     g4.create_state((3,4)) # B
        self.assertEquals(g5.to_move_colour(), WHITE)
        self.assertEquals(g5.terminal(), False)
        board = g5.board()
        self.assertEquals(board.get_occ((0,1)), BLACK)
        self.assertEquals(board.get_occ((1,3)), BLACK)
        self.assertEquals(board.get_occ((3,4)), BLACK)
        self.assertEquals(board.get_occ((1,2)), EMPTY)
        self.assertEquals(board.get_occ((2,3)), EMPTY)

class BoardUtilityTests(unittest.TestCase):
    def setUp(self):
        player1 = human_player.HumanPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(5, "standard")
        my_game = game.Game(r, player1, player2)
        self.s = ABState()
        self.s.set_state(my_game.current_state)

    '''
    def testCompareTwoMoves(self):
        g1 = self.s.create_state((0,1)) # B
        g2 =     g1.create_state((1,2)) # W
        g3 =     g2.create_state((1,3)) # B
        g4 =     g3.create_state((2,3)) # W
        g5 =     g4.create_state((3,4)) # B
        self.assertEquals(g5.to_move_colour(), WHITE)
        self.assertEquals(g5.terminal(), False)
        board = g5.board()
        self.assertEquals(board.get_occ((0,1)), BLACK)
    '''


if __name__ == "__main__":
    unittest.main()

