#!/usr/bin/env python

import unittest
#import mock

import pdb

from board import *
from update_substrips import *


class BoardTest(unittest.TestCase):
    def test_create_board(self):
        board = Board(size = 13)
        self.assertEquals(board.size, 13)

    def test_empty_board_score_stats(self):
        board = Board(size = 13)
        # self.assertEquals(board.score(), 0) TODO

    def test_empty_board_place_one_piece(self):
        self.us_counter = LengthCounter()
        self.them_counter = LengthCounter()

        board = Board(size = 13)
        #pdb.set_trace()
        # TODO board.make_move(7,7)
        #self.assertEquals() TODO

if __name__ == "__main__":
    unittest.main()



