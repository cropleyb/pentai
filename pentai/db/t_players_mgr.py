#!/usr/bin/env python

import os
import unittest

from pentai.base.human_player import *
from pentai.ai.ai_player import *
import pentai.db.test_db as test_db

from ai_factory import *
from players_mgr import *

class AIFactoryTest(unittest.TestCase):

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

    def test_ai_restore_player2(self):
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
        test_db.init()

    def tearDown(self):
        test_db.clear_all()

    # !python ./pentai/db/t_players_mgr.py HumanDBTest.test_human_save_to_db
    def test_human_save_to_db(self):
        db = PlayersMgr(prefix="test_")
        p = HumanPlayer("Sandra")
        db.save(p)

        fp = db.find_by_name("Sandra")
        self.assertEquals(fp.__class__, HumanPlayer)
        self.assertEquals(fp.get_name(), "Sandra")

    def test_rename_ai(self):
        db = PlayersMgr(prefix="test_")
        genome = AIGenome("Hagrid")
        genome.max_depth = 3
        db.save(genome)

        gp = db.find_genome_by_name("Hagrid")

        genome.p_name = "Hagrid2"
        db.save(genome)

        gp = db.find_genome_by_name("Hagrid")
        self.assertEquals(gp, None)

        gp = db.find_genome_by_name("Hagrid2")

        self.assertEquals(gp.__class__, AIGenome)
        self.assertEquals(gp.get_name(), "Hagrid2")
        self.assertEquals(gp.max_depth, 3)

class RecentUseTest(unittest.TestCase):
    def setUp(self):
        test_db.init()

    def tearDown(self):
        test_db.clear_all()

    '''
    def mark_recent_player(self, player):
    def get_recent_player_names(self, player_type, number):
    def get_ai_player_names(self):
    def get_human_player_names(self):
    def get_recent_players(self, player_type, number):
    def remove(self, pid):
    def save(self, player, update_cache=True):
    def find_by_name(self, name, player_type=None, update_cache=True):
    def find_genome_by_name(self, name, player_type=None, update_cache=True):
    def find(self, p_key, update_cache=True):
    def get_player_name(self, p_key):
    '''

    def test_human_save_to_db(self):
        db = PlayersMgr(prefix="test_")
        fp = db.find_by_name("Sandra")
        self.assertEquals(fp, None)
        p = HumanPlayer("Sandra")
        db.save(p)

        fp = db.find_by_name("Sandra")
        self.assertEquals(fp.get_name(), "Sandra")

        pl = db.get_recent_genomes("Human", 10)
        self.assertEquals(len(pl), 1)
        self.assertEquals(pl[0].get_name(), "Sandra")

        pl = db.get_recent_genomes("AI", 10)
        self.assertEquals(len(pl), 0)

        pl = db.get_recent_player_names("Human", 10)
        self.assertEquals(len(pl), 1)
        self.assertEquals(pl[0], "Sandra")

    def test_mark_recent_human(self):
        db = PlayersMgr(prefix="test_")
        p1 = HumanPlayer("Sandra")
        db.save(p1)
        p2 = HumanPlayer("Oscar")
        db.save(p2)

        pl = db.get_recent_player_names("Human", 1)
        self.assertEquals(pl[0], "Oscar")
        self.assertEquals(len(pl), 1)

        db.mark_recent_player(p1)
        pl = db.get_recent_player_names("Human", 1)
        self.assertEquals(len(pl), 1)
        self.assertEquals(pl[0], "Sandra")

if __name__ == "__main__":
    unittest.main()
