#!/usr/bin/env python

import unittest

from ai_factory import *
from ai_player_db import *
from human_player import *

class AIFactoryTest(unittest.TestCase):
    def test_ai_restore_player(self):
        genome = Genome("Samuel")
        genome.max_depth = 3
        aif = AIFactory()
        orig_player = aif.create_player(genome)

        db = PlayerDB('test_player.pkl')
        db.add(orig_player)

        rp = db.find("Samuel")

        self.assertEquals(rp.__class__, AIPlayer)
        self.assertEquals(rp.name, "Samuel")
        self.assertEquals(rp.max_depth, 3)

class HumanDBTest(unittest.TestCase):
    def test_human_save_to_db(self):
        db = PlayerDB('test_player.pkl')
        p = HumanPlayer("Sandra")
        db.add(p)

        fp = db.find("Sandra")
        self.assertEquals(fp.__class__, HumanPlayer)
        self.assertEquals(fp.name, "Sandra")

if __name__ == "__main__":
    unittest.main()
