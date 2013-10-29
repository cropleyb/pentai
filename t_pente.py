#!/usr/bin/env python

import unittest
#import mock

import pdb

from pente import *


class GameTest(unittest.TestCase):
    def test_create_game(self):
        game = Game(size = 13)
        self.assertEquals(game.board.size, 13)

    def test_empty_board_score_stats(self):
        game = Game(size = 13)
        self.assertEquals(game.current_state.score(), 0)

    def test_empty_board_place_one_piece(self):
        game = Game(size = 13)
        pdb.set_trace()
        game.make_move(7,7)
        self.assertEquals()
        # This is failing because of the global BOARD_SIZE

if __name__ == "__main__":
    unittest.main()



