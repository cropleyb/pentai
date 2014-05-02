#!/usr/bin/env python

import unittest

from pentai.base.game_state import *
from pentai.base.game import *
from pentai.base.rules import *
from pentai.ai.standardise import *

class StandardiseTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "standard")
        self.game = Game(self.rules, p_m.Player("BC"), p_m.Player("Whoever"))

    def test_flip_and_shift(self): # TODO: rename to flip
        self.game.load_moves("1. (10,10)\n2. (11,9)")
        std, fwd, rev = standardise(self.game.current_state)

        #brd = std.get_board()
        self.assertEqual(std.get_all_captured(), [0, 0, 0])
        print std
        #self.assertEqual(brd.get_occ((0,8)), BLACK)


if __name__ == "__main__":
    unittest.main()
