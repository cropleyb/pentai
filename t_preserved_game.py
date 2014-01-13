
#!/usr/bin/env python

import unittest
from game import *
from persistent_dict import *
from priority_filter_2 import *
from ai_player import *
from rules import *
from preserved_game import *
from games_db import *

import pdb

class PreservedGameTest(unittest.TestCase):
    def setUp(self):
        pass

    def create_player(self, name, mmpdl, narrowing, chokes):
        sf = PriorityFilter2()
        return AIPlayer(sf, name=name)

    def test_preserve_game(self):
        chokes = [(4,3),(5,1)]
        p1 = self.create_player("Sonia", 9, 0, chokes)
        p2 = self.create_player("Toby", 9, 0, chokes)

        r = Rules(13, "standard")
        orig_game = Game(r, p1, p2)

        pg = PreservedGame(orig_game)
        apg = GamesDB("test_games.pkl")
        apg.add(pg)
        #self.assertEquals(len(l), 0)

if __name__ == "__main__":
    unittest.main()

