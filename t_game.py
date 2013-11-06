#!/usr/bin/env python

import unittest

from game import *

class GameTest(unittest.TestCase):
    def test_create_game(self):
        board = Board(size = 13)
        self.assertEquals(board.size, 13)

    def test_empty_board_score_stats(self):
        board = Board(size = 13)
        self.assertEquals(board.score(), 0)

    def test_empty_board_place_one_piece(self):
        self.us_counter = LengthCounter()
        self.them_counter = LengthCounter()

        board = Board(size = 13)
        #pdb.set_trace()
        board.make_move(7,7)
        #self.assertEquals() TODO

if __name__ == "__main__":
    unittest.main()



