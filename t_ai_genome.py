#!/usr/bin/env python

import unittest

from ai_genome import *

class AIGenomeTest(unittest.TestCase):
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

