#!/usr/bin/env python

import unittest

import gui
import human_player
import rules
import game

from simpleton import *

class SimpletonPlayerTest(unittest.TestCase):

    def setUp(self):
        # TODO
        player1 = SimpletonPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(5, "standard")
        self.game = game.Game(r, player1, player2)
        self.gui = None

    def test_find_one_move(self):
        p = SimpletonPlayer("Dur")
        p.prompt_for_action(self.game, self.gui)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, gui.MoveAction.create_from_tuple(2,2))

if __name__ == "__main__":
    unittest.main()


