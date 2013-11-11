#!/usr/bin/env python

import unittest

import pdb

from board_strip import *

class BoardStripTest(unittest.TestCase):
    def test_empty_board_strip_is_empty(self):
        strip = BoardStrip()
        self.assertEquals(strip.get_occ(0), EMPTY)

    def test_empty_strip_place_one_black_piece(self):
        strip = BoardStrip()
        strip.set_occ(0, BLACK)
        self.assertEquals(strip.get_occ(0), BLACK)

    def test_empty_strip_place_one_white_piece(self):
        strip = BoardStrip()
        strip.set_occ(1, WHITE)
        self.assertEquals(strip.get_occ(1), WHITE)

    def test_empty_strip_place_one_white_piece_far(self):
        strip = BoardStrip()
        strip.set_occ(18, WHITE)
        self.assertEquals(strip.get_occ(18), WHITE)

    def test_empty_strip_place_one_black_piece_far(self):
        strip = BoardStrip()
        strip.set_occ(18, BLACK)
        self.assertEquals(strip.get_occ(18), BLACK)

    def test_place_two_pieces(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(2, BLACK)
        self.assertEquals(strip.get_occ(1), BLACK)
        self.assertEquals(strip.get_occ(2), BLACK)

    def test_place_two_pieces_widely(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(21, WHITE)
        self.assertEquals(strip.get_occ(1), BLACK)
        self.assertEquals(strip.get_occ(21), WHITE)
        self.assertEquals(strip.get_occ(13), EMPTY)
'''
    def test_empty_board_place_one_piece_in_zero_corner(self):
        board = Board(size = 7)
        board.set_occ(Pos(0, 0), BLACK)
        self.assertEquals(board.get_occ(Pos(0, 0)), BLACK)

    def test_empty_board_place_one_piece_in_big_corner(self):
        board = Board(size = 7)
        board.set_occ(Pos(7, 7), WHITE)
        self.assertEquals(board.get_occ(Pos(7, 7)), WHITE)

    #########################################
    # pos in line through pos for substrips #
    #########################################
    def test_get_positions_in_E_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (1,0), 4)
        self.assertEquals(piltp,
                [(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7)])

    def test_get_positions_in_SE_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (1,1), 4)
        self.assertEquals(piltp,
                [(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11)])

    def test_get_positions_in_S_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (0,1), 4)
        self.assertEquals(piltp,
                [(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11)])

    def test_get_positions_in_SW_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (-1,1), 4)
        self.assertEquals(piltp,
                [(11,3),(10,4),(9,5),(8,6),(7,7),(6,8),(5,9),(4,10),(3,11)])
'''


if __name__ == "__main__":
    unittest.main()



