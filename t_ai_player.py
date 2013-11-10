#!/usr/bin/env python

import unittest

import pdb
import gui
import human_player
import rules
import game
#import profile

from ai_player import *

class AIPlayerTest(unittest.TestCase):

    def setUp(self):
        # TODO
        player1 = AIPlayer("Blomp")
        player2 = human_player.HumanPlayer("Kubba")
        r = rules.Rules(13, "standard")
        self.game = game.Game(r, player1, player2)
        self.gui = None
        '''
        self.s = ABState()
        self.s.set_state(my_game.current_state)
        '''

    def test_find_one_move(self):
        p = AIPlayer("Deep thunk")
        pdb.set_trace()
        p.prompt_for_action(self.game, self.gui)
        ma = p.get_action(self.game, self.gui)
        self.assertEquals(ma, gui.MoveAction(6,6))

if __name__ == "__main__":
    unittest.main()



