#!/usr/bin/env python

import unittest

from ai_factory import *
from ai_player_db import *

class AIFactoryTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_genome_valid_field(self):
        genome = Genome("Happy")
        genome.max_depth = 7
        self.assertEquals(genome.max_depth, 7)

    def test_set_genome_invalid_field(self):
        genome = Genome("Sad")
        try:
            genome.botter_snipes = "FDSJKL"
        except GenomeException, e:
            return
        self.fail()
    
    def test_ai_factory_create_from_genome(self):
        genome = Genome("Freddo Frog")
        genome.max_depth = 8
        aif = AIFactory()
        p = aif.create_player(genome)

        self.assertEquals(p.max_depth, 8)

    def test_restore_player(self):
        genome = Genome("Samuel")
        genome.max_depth = 3
        aif = AIFactory()
        orig_player = aif.create_player(genome)

        db = AIPlayerDB('test_ai.pkl')
        db.add(orig_player)

        rp = db.find("Samuel")

        self.assertEquals(rp.__class__, AIPlayer)
        self.assertEquals(rp.name, "Samuel")
        self.assertEquals(rp.max_depth, 3)

