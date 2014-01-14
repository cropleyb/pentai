#!/usr/bin/env python

import rules
import game

import time

from ai_player import *
from priority_filter import *
from priority_filter_2 import *
from blindness_filter import *
from evaluator import *

import pdb


import pstats, cProfile

class GenomeException(Exception):
    pass

class Genome(object):
    def __init__(self, name):
        defaults = {
            "name": name,
            # Search params
            "max_depth": 6,
            "max_depth_boost": 0,
            "mmpdl": 9,
            "narrowing": 0,
            "chokes": [(4,2)],
            "filter2": False,
            # Utility function
            "capture_score_base": 300,
            "take_score_base": 100,
            "threat_score_base": 20,
            "captures_scale": [0, 1, 1, 1, 1, 1],
            "length_factor": 27,
            "move_factor": 30,
            "blindness": 0,
            "sub": True,
        }
        super(Genome, self).__setattr__("__dict__", defaults)

    def __setattr__(self, attr_name, val):
        if not hasattr(self, attr_name):
            raise GenomeException("Cannot set attribute %s" % attr_name)
        super(Genome, self).__setattr__(attr_name, val)

    def key(self):
        return self.name

class AIFactory:
    def __init__(self):
        pass

    def create_player(self, genome):
        if genome.filter2:
            sf = PriorityFilter2()
        else:
            sf = PriorityFilter()
        sf.set_max_moves_per_depth_level(mmpdl=genome.mmpdl, narrowing=genome.narrowing,
                chokes=genome.chokes)
        if genome.blindness > 0:
            bf = BlindnessFilter(sf)
            bf.set_blindness(genome.blindness)
            sf = bf
        p = AIPlayer(sf, name=genome.name)
        p.set_max_depth(genome.max_depth + genome.max_depth_boost)
        self.set_config(genome, p)
        p.genome = genome

        return p

    def set_config(self, genome, player):
        uc = player.get_utility_calculator()
        uc.capture_score_base = genome.capture_score_base
        uc.take_score_base = genome.take_score_base
        uc.threat_score_base = genome.threat_score_base
        uc.captures_scale = genome.captures_scale
        uc.length_factor = genome.length_factor
        uc.move_factor = genome.move_factor
        uc.sub = genome.sub

