#!/usr/bin/env python

import unittest

from ai_factory import *

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

