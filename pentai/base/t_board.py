#!/usr/bin/env python

import unittest

from pentai.base.board import *

class BoardTest(unittest.TestCase):
    def test_create_board(self):
        board = Board(size = 13)
        self.assertEquals(board.size, 13)

    def test_empty_board_is_empty(self):
        board = Board(size = 13)
        self.assertEquals(board.get_occ((1, 5)), EMPTY)

    def test_empty_board_place_one_black_piece(self):
        board = Board(size = 13)
        board.set_occ((0, 1), P1)
        self.assertEquals(board.get_occ((0, 1)), P1)

    def test_empty_board_place_one_white_piece(self):
        board = Board(size = 7)
        board.set_occ((2, 3), P2)
        self.assertEquals(board.get_occ((2, 3)), P2)

    def test_empty_board_place_one_piece_in_zero_corner(self):
        board = Board(size = 7)
        board.set_occ((0, 0), P1)
        self.assertEquals(board.get_occ((0, 0)), P1)

    def test_empty_board_place_one_piece_in_big_corner(self):
        board = Board(size = 7)
        board.set_occ((6, 6), P2)
        self.assertEquals(board.get_occ((6, 6)), P2)

    def test_board_place_one_piece_in_big_corner_then_remove(self):
        board = Board(size = 7)
        board.set_occ((6, 6), P2)
        board.set_occ((6, 6), EMPTY)
        self.assertEquals(board.get_occ((6, 6)), EMPTY)

    def test_place_off_board_raises_exception(self):
        board = Board(size = 7)
        try:
            board.set_occ((7,7), P2)
        except OffBoardException:
            return
        self.fail()

if __name__ == "__main__":
    unittest.main()



