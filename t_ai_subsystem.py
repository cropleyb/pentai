#!/usr/bin/env python

import unittest

import gui
import human_player
import rules
import game

from ai_player import *

import pdb

class AIPlayerSubsystemTest(unittest.TestCase):

    def setUp(self):
        self.p1 = AIPlayer(name="Deep thunk", mmpdl=9, narrowing=0)
        self.p2 = AIPlayer(name="Deep thunk2", mmpdl=9, narrowing=0)
        r = rules.Rules(13, "standard")
        self.game = game.Game(r, self.p1, self.p2)

    # !./t_ai_subsystem.py AIPlayerSubsystemTest.test_find_one_move
    def test_find_one_move(self):
        self.p2.set_max_depth(2)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (7, 7)
3. (8, 6)
4. (9, 6)
5. (6, 4)
6. (9, 7)
7. (9, 8)
8. (9, 5)
9. (6, 5)
10. (6, 7)
11. (8, 7)
12. (9, 4)
13. (9, 3)
14. (7, 6)
15. (6, 3)
16. (6, 2)
17. (5, 7)
"""
        self.game.load_game(game_str)
        m = self.p2.do_the_search()
        self.assertEquals(m, (6,7))

    # !./t_ai_player.py AIPlayerSubsystemTest.test_dont_waste_a_pair
    def test_dont_waste_a_pair(self):
        self.p1.set_max_depth(6)
        game_str = \
"""Black versus White
13x13
standard rules
1. (6, 6)
2. (6, 7)
3. (8, 8)
4. (5, 5)
5. (8, 6)
6. (7, 6)
7. (8, 5)
8. (8, 7)
9. (8, 4)
10. (5, 8)
"""
        self.game.load_game(game_str)
        m = self.p1.do_the_search()
        self.assertNotEquals(m, (6,5))

if __name__ == "__main__":
    unittest.main()
