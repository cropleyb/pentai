#!/usr/bin/env python

import unittest

import gui
import human_player
import rules
import game

from ai_player import *

import pdb

def MA(x, y):
    return gui.MoveAction.create_from_tuple(x,y)

class AIPlayerTest(unittest.TestCase):

    def setUp(self):
        self.p1 = AIPlayer(1, "Deep thunk")
        self.p2 = AIPlayer(1, "Deep thunk2")
        r = rules.Rules(9, "standard")
        self.game = game.Game(r, self.p1, self.p2)
        self.p1.attach_to_game(self.game)
        self.p2.attach_to_game(self.game)
        self.gui = None

    def test_find_one_move(self):
        p = self.p1
        p.prompt_for_action(self.game, self.gui, test=True)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, MA(4,4))

    def test_respond_to_corner_start(self):
        self.game.make_move((0,0))

        p = self.p2
        p.prompt_for_action(self.game, self.gui, test=True)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, MA(2,2))

    def test_respond_to_centre_start(self):
        self.game.make_move((4,4))

        p = self.p2
        p.prompt_for_action(self.game, self.gui, test=True)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, MA(3,4))

        #pdb.set_trace()
if __name__ == "__main__":
    unittest.main()

