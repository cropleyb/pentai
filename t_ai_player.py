#!/usr/bin/env python

import unittest

import gui
import human_player
import rules
import game
#import profile

from ai_player import *

class AIPlayerTest(unittest.TestCase):

    def setUp(self):
        # TODO
        player1 = AIPlayer(2, "Blomp", BLACK)
        player2 = human_player.HumanPlayer("Kubba", WHITE)
        r = rules.Rules(5, "standard")
        self.game = game.Game(r, player1, player2)
        self.gui = None

    def test_find_one_move(self):
        p = AIPlayer(2, "Deep thunk", BLACK)
        p.attach_to_game(self.game)
        p.prompt_for_action(self.game, self.gui, test=True)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, gui.MoveAction.create_from_tuple(2,2))

if __name__ == "__main__":
    unittest.main()

