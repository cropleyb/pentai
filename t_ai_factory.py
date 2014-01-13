#!/usr/bin/env python

import unittest

from ai_factory import *

class GameTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_genome_valid_field(self):
        genome = Genome("Happy")
        genome.max_depth = 7

    def test_set_genome_invalid_field(self):
        genome = Genome("Sad")
        try:
            genome.botter_snipes = "FDSJKL"
        except GenomeException, e:
            return
        self.fail()
    '''
    def test_ai_factory(self):
        genome = Genome("Freddo Frog")
        aif = AIFactory()
        p = aif.create_ai(genome)

        #self.assertEquals(game.get_move_number(), 3)
    '''
