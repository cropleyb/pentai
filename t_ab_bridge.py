#!/usr/bin/env python

import unittest

import pdb

import ab_bridge
import alpha_beta


class AlphaBetaBridgeTest(unittest.TestCase):

    def test_one_level_search(self):
        g = ab_bridge.ABGame(7)

        pdb.set_trace()

        alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
        # self.assertEquals() # TODO


if __name__ == "__main__":
    unittest.main()



