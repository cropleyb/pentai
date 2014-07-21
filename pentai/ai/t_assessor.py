#!/usr/bin/env python

import unittest

import pentai.base.rules as r_m
import pentai.base.game as g_m

from pentai.ai.assessor import *

import pentai.db.ai_factory as aif_m
import pentai.ai.ai_genome as aig_m

class AssessorTest(unittest.TestCase):
    def create_player(self):
        aif = aif_m.AIFactory()
        genome = aig_m.AIGenome("AIPlayer")
        genome.use_openings_book = False
        return aif.create_player(genome)

    def setUp(self):
        self.p1 = self.create_player()
        self.p2 = self.create_player()

        r = r_m.Rules(13, "standard")
        self.game = g_m.Game(r, self.p1, self.p2)

    def test_calc_winning_best(self):
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 5)
3. (6, 7)
4. (9, 6)
5. (6, 8)
6. (9, 7)
7. (6, 9)
8. (9, 5)
9. (7, 2)
"""
        self.game.load_game(game_str)

        a = Assessor(self.game)
        a.set_turn_number(9)
        best = a.calc_best_move(gui=None)
        turn, prev_move, best_move = best

        self.assertEquals(turn, 9)
        self.assertEquals(prev_move, (9,5))
        self.assertEquals(best_move, (6,10))

    # TODO
    # check that we don't interfere with the original game

if __name__ == "__main__":
    unittest.main()



