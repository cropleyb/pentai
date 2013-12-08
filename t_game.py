#!/usr/bin/env python

import unittest

from game import *

class GameTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_game(self):
        board = Board(size = 9)
        game = Game(board, None, None)
        game.load_game("1. (4, 4)\n2. (3, 3)\n")

        self.assertEquals(game.get_move_number(), 3)


if __name__ == "__main__":
    unittest.main()



