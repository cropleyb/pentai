#!/usr/bin/python

import games_mgr as gm_m
import openings_book as ol_m
import human_player as h_m
import players_mgr as pm_m
import ai_genome as aig_m
from defines import *

import sys
import os

def dot():
    sys.stdout.write('.')
    sys.stdout.flush()

if __name__ == "__main__":
    print "Creating Human Players"
    pm = pm_m.PlayersMgr()

    for name in ["BC", "Bruce", "Jespah", "Arwen", "Sascha"]:
        h = h_m.HumanPlayer(name)
        dot()
        pm.save(h)

    genome = aig_m.AIGenome("")
    
    players = [
    { "p_name": "Deep Thunk", "use_openings_book": True, "max_depth": 10,
        "mmpdl": 9, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Pentachov", "use_openings_book": True, "max_depth": 8,
        "mmpdl": 9, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Killer", "use_openings_book": True, "max_depth": 6,
        "mmpdl": 9, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Sonja", "use_openings_book": True, "max_depth": 4,
        "mmpdl": 9, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Renaldo", "use_openings_book": True, "max_depth": 2,
        "mmpdl": 12, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Stephanie", "use_openings_book": True, "max_depth": 6,
        "mmpdl": 9, "vision": 90, "capture_score_base": 300 },
    { "p_name": "Professor", "use_openings_book": False, "max_depth": 10,
        "mmpdl": 9, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Andrea", "use_openings_book": False, "max_depth": 4,
        "mmpdl": 9, "vision": 95, "capture_score_base": 300 },
    { "p_name": "Tamazin", "use_openings_book": False, "max_depth": 4,
        "mmpdl": 9, "vision": 90, "capture_score_base": 200 },
    { "p_name": "Wei", "use_openings_book": False, "max_depth": 4,
        "mmpdl": 9, "vision": 85, "capture_score_base": 300 },
    { "p_name": "Gretel", "use_openings_book": False, "max_depth": 4,
        "mmpdl": 9, "vision": 80, "capture_score_base": 400 },
    { "p_name": "JJ", "use_openings_book": False, "max_depth": 6,
        "mmpdl": 4, "vision": 75, "capture_score_base": 300 },
    { "p_name": "Sam", "use_openings_book": False, "max_depth": 4,
        "mmpdl": 9, "vision": 70, "capture_score_base": 300 },
    { "p_name": "Scott", "use_openings_book": False, "max_depth": 2,
        "mmpdl": 6, "vision": 65, "capture_score_base": 300 },
    { "p_name": "Tony", "use_openings_book": False, "max_depth": 1,
        "mmpdl": 6, "vision": 60, "capture_score_base": 400 },
    ]
    st()
    for p in players:
        genome.__dict__.update(p)
        dot()
        p = pm.find_by_name(genome.p_name, "Computer")
        if p:
            genome.p_key = p.p_key
        else:
            genome.p_key = pm.next_id()

        pm.save(genome.clone())

