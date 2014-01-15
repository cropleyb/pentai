#!/usr/bin/env python

import unittest

from ai_factory import *

class AIFactoryTest(unittest.TestCase):
    def test_ai_factory_create_from_genome(self):
        genome = Genome("Freddo Frog")
        genome.max_depth = 8
        aif = AIFactory()
        p = aif.create_player(genome)

        self.assertEquals(p.max_depth, 8)

