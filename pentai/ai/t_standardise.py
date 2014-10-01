#!/usr/bin/env python

import unittest

from pentai.base.game_state import *
from pentai.base.game import *
import pentai.base.player as p_m
from pentai.base.rules import *
from pentai.ai.standardise import *
from pentai.base.direction_strips import *


class StandardiseTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "standard")
        self.game = Game(self.rules, p_m.Player("BC"), p_m.Player("Whoever"))

    #!python ./pentai/ai/t_standardise.py StandardiseTest.test_diagonals
    def test_diagonals(self):
        for i in range(0,19):
            self.diagonals_check(i)

    def diagonals_check(self, i):
        self.game.load_moves("1. (%s,%s)" % (i,i))
        std, fwd, rev = standardise(self.game.current_state)
        std_ii = fwd(i, i)

        if i < 5:
            self.assertEquals(std_ii, (18-i, i))
        elif i > 13:
            self.assertEquals(std_ii, (i, 18-i))
        else:
            self.assertEquals(std_ii, (5, 5))

        self.game.go_to_the_beginning()

    def test_rot_and_shift(self):
        self.game.load_moves("1. (8,7)\n2. (10,11)")
        std, fwd, rev = standardise(self.game.current_state)

        ds = EDirectionStrips(19)
        ds._override(std)
        # Useful... don't cull everywhere
        #brd = self.game.get_board()
        #brd.d_strips[0] = ds
        #log.debug(ds.strips)
        #log.debug(brd)

        self.assertEqual(ds.get_occ((5,7)), P1)
        self.assertEqual(ds.get_occ((9,5)), P2)

    def test_standardisation_trims_array(self):
        self.game.load_moves("1. (8,7)")
        std, fwd, rev = standardise(self.game.current_state)

        self.assertEqual(len(std), 6)

if __name__ == "__main__":
    unittest.main()
