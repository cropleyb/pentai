#!/usr/bin/env python

import unittest

from board import *

class BoardTest(unittest.TestCase):
    def test_create_board(self):
        board = Board(size = 13)
        self.assertEquals(board.size, 13)

    def test_empty_board_is_empty(self):
        board = Board(size = 13)
        self.assertEquals(board.get_occ((1, 5)), EMPTY)

    def test_empty_board_place_one_black_piece(self):
        board = Board(size = 13)
        board.set_occ((0, 1), BLACK)
        self.assertEquals(board.get_occ((0, 1)), BLACK)

    def test_empty_board_place_one_white_piece(self):
        board = Board(size = 7)
        board.set_occ((2, 3), WHITE)
        self.assertEquals(board.get_occ((2, 3)), WHITE)

    def test_empty_board_place_one_piece_in_zero_corner(self):
        board = Board(size = 7)
        board.set_occ((0, 0), BLACK)
        self.assertEquals(board.get_occ((0, 0)), BLACK)

    def test_empty_board_place_one_piece_in_big_corner(self):
        board = Board(size = 7)
        board.set_occ((7, 7), WHITE)
        self.assertEquals(board.get_occ((7, 7)), WHITE)

if __name__ == "__main__":
    unittest.main()



