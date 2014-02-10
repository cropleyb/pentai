#!/usr/bin/env python

import ai_player
from priority_filter import *
from priority_filter_2 import *

import openings_book as ob_m
import games_mgr

from ai_genome import *

class AIFactory: # TODO: These are just functions

    def create_player(self, genome):
        if genome.filter2:
            sf = PriorityFilter2()
        else:
            sf = PriorityFilter()
        sf.set_max_moves_per_depth_level(mmpdl=genome.mmpdl, narrowing=genome.narrowing,
                chokes=genome.chokes)
        try:
            vision = genome.vision
        except AttributeError:
            vision = 100
        sf.set_vision(vision)

        try:
            p_name = genome.p_name
        except AttributeError:
            p_name = genome.name
        p = ai_player.AIPlayer(sf, p_name=p_name)

        try:
            p_key = genome.p_key
        except AttributeError:
            p_key = genome.key
        p.p_key = p_key
        
        if genome.use_openings_book:
            ob = ob_m.instance
            if not ob:
                gm = games_mgr.GamesMgr()
                ob = ob_m.OpeningsBook(gm)
                ob_m.instance = ob
            p.set_use_openings_book(ob)

        p.force_depth = genome.force_depth

        genome.set_override(True)
        p.set_max_depth(genome.max_depth + genome.max_depth_boost)
        genome.set_override(False)

        self.set_utility_config(genome, p)
        p.genome = genome

        return p

    def set_utility_config(self, genome, player):
        uc = player.get_utility_calculator()
        uc.capture_score_base = genome.capture_score_base
        uc.take_score_base = genome.take_score_base
        uc.threat_score_base = genome.threat_score_base
        uc.captures_scale = genome.captures_scale
        uc.move_factor = genome.move_factor

        uc.length_factor = genome.length_factor
        uc.use_net_captures = genome.use_net_captures
        uc.length_scale = genome.length_scale
        uc.scale_pob = genome.scale_pob
        uc.calc_mode = genome.calc_mode

        genome.set_override(True)
        try:
            uc.misjudgement = genome.misjudgement
        except:
            uc.misjudgement = genome.misjudgement = 0
        '''
        # Example of how to handle new fields:
        try:
            uc.length_scale = genome.length_scale
        except:
            uc.length_scale = genome.length_scale = [1,1,1,1,1,1]
        # Then run upgrade_dbs.py
        '''
        genome.set_override(False)

