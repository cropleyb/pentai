#!/usr/bin/env python

import unittest

import pdb

import ab_bridge
import alpha_beta

import game
import rules


class AlphaBetaBridgeTest(unittest.TestCase):

    def test_one_level_search(self):
        r = rules.Rules(7, "standard")
        '''
        # TODO
        player1 = AIPlayer()
        my_game = game.Game(player1, player2)
        # def __init__(self, rules, player1, player2):
        g = ab_bridge.ABGame(my_game)

        # pdb.set_trace()

        alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
        # self.assertEquals() # TODO
        '''


if __name__ == "__main__":
    unittest.main()



