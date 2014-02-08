#!/usr/bin/env python

import os
import unittest

from ai_factory import *
from players_mgr import *
from human_player import *
from ai_player import *

class AIFactoryTest(unittest.TestCase):
    def setUp(self):
        self.test_db_filename = 'test_players.pkl'

    def tearDown(self):
        os.unlink(self.test_db_filename)

    def test_ai_restore_player(self):
        genome = AIGenome("Samuel")
        genome.max_depth = 3
        aif = AIFactory()
        orig_player = aif.create_player(genome)

        db = PlayersMgr(prefix="test_")
        db.save(orig_player)

        rp = db.find_by_name("Samuel")

        self.assertEquals(rp.__class__, AIPlayer)
        self.assertEquals(rp.get_name(), "Samuel")
        self.assertEquals(rp.max_depth, 3)

    def test_ai_restore_player(self):
        genome = AIGenome("Hagrid")
        genome.max_depth = 3
        aif = AIFactory()
        orig_player = aif.create_player(genome)

        db = PlayersMgr(prefix="test_")
        gp = db.find_genome_by_name("Hagrid")
        self.assertIsNone(gp)
        db.save(orig_player)

        gp = db.find_genome_by_name("Hagrid")

        self.assertEquals(gp.__class__, AIGenome)
        self.assertEquals(gp.get_name(), "Hagrid")
        self.assertEquals(gp.max_depth, 3)

class HumanDBTest(unittest.TestCase):
    def setUp(self):
        self.test_db_filename = 'test_players.pkl'

    def tearDown(self):
        os.unlink(self.test_db_filename)

    def test_human_save_to_db(self):
        db = PlayersMgr(prefix="test_")
        p = HumanPlayer("Sandra")
        db.save(p)

        fp = db.find_by_name("Sandra")
        self.assertEquals(fp.__class__, HumanPlayer)
        self.assertEquals(fp.get_name(), "Sandra")

if __name__ == "__main__":
    unittest.main()
