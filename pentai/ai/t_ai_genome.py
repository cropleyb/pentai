#!/usr/bin/env python

import unittest

from pentai.ai.ai_genome import *

class AIGenomeTest(unittest.TestCase):
    def test_set_genome_valid_field(self):
        genome = AIGenome("Happy")
        genome.max_depth = 7
        self.assertEquals(genome.max_depth, 7)

    def test_set_genome_invalid_field(self):
        genome = AIGenome("Sad")
        try:
            genome.botter_snipes = "FDSJKL"
        except AIGenomeException, e:
            return
        self.fail()

