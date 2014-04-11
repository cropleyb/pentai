#!/usr/bin/env python

import unittest

import pentai.base.rules as r_m
import pentai.base.game as g_m

from pentai.ai.ai_player import *
import pentai.ai.ai_genome as aig_m
import pentai.db.ai_factory as aif_m

class AIPlayerTest(unittest.TestCase):

    def create_player(self, name, mmpdl, narrowing):
        aig = aig_m.AIGenome(name)
        aif = aif_m.AIFactory()
        aig.use_openings_book = False # override to make it deterministic
        aig.max_depth = 1
        player = aif.create_player(aig)

        return player

    def setUp(self):
        self.p1 = self.create_player("Deep thunk", 9, 0)
        self.p2 = self.create_player("Deep thunk2", 9, 0)
        r = r_m.Rules(9, "standard")
        self.game = g_m.Game(r, self.p1, self.p2)
        self.p1.attach_to_game(self.game)
        self.p2.attach_to_game(self.game)
        self.gui = None

    def test_find_one_move(self):
        p = self.p1
        ma = p.prompt_for_action(self.game, self.gui, test=True)
        self.assertEquals(ma, (4,4))

    def test_respond_to_corner_start(self):
        self.game.make_move((0,0))

        p = self.p2
        ma = p.prompt_for_action(self.game, self.gui, test=True)
        self.assertEquals(ma, (4,4))

    def test_respond_to_centre_start(self):
        self.game.make_move((4,4))

        p = self.p2
        ma = p.prompt_for_action(self.game, self.gui, test=True)
        self.assertIn(ma, [(5,5),(3,3),(5,4)])

if __name__ == "__main__":
    unittest.main()

