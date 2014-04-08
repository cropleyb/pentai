#!/usr/bin/python

import pentai.db.games_mgr as gm_m
import pentai.db.openings_book as ol_m
import pentai.base.human_player as h_m
import pentai.db.players_mgr as pm_m
import pentai.ai.ai_genome as aig_m
from pentai.base.defines import *

import sys
import os

def dot():
    sys.stdout.write('.')
    sys.stdout.flush()

if __name__ == "__main__":
    print "Creating Human Players"
    '''
    app_supp_dir = "/Users/cropleyb/Library/Application Support/pentai/db/"

    pm = pm_m.PlayersMgr(prefix=app_supp_dir)
    '''
    pm = pm_m.PlayersMgr()

    # TODO: Don't release these.
    player_names = ["BC", "Bruce", "Mark", "Jespah", "Arwen", "Sascha",
            "Marion", "Wendy"]

    player_names.reverse()
    for name in player_names:
        h = pm.find_by_name(name, "Human")
        if not h:
            h = h_m.HumanPlayer(name)
        dot()
        pm.save(h)

    #sys.exit()
    print "Creating Computer Players"
    genome = aig_m.AIGenome("")
    
    players = [
    { "p_name": "Samuel", "use_openings_book": True, "max_depth": 10,
        "judgement": 100, "vision": 100, "capture_score_base": 350 },
    { "p_name": "Reanne", "use_openings_book": True, "max_depth": 9,
        "judgement": 95, "vision": 95, "capture_score_base": 350 },
    { "p_name": "Quentin", "use_openings_book": True, "max_depth": 9,
        "judgement": 90, "vision": 90, "capture_score_base": 350 },
    { "p_name": "Petunia", "use_openings_book": True, "max_depth": 8,
        "judgement": 85, "vision": 85, "capture_score_base": 350 },
    { "p_name": "Oscar", "use_openings_book": True, "max_depth": 8,
        "judgement": 80, "vision": 80, "capture_score_base": 350 },
    { "p_name": "Noreen", "use_openings_book": True, "max_depth": 7,
        "judgement": 75, "vision": 75, "capture_score_base": 350 },
    { "p_name": "Marmaduke", "use_openings_book": True, "max_depth": 7,
        "judgement": 70, "vision": 70, "capture_score_base": 350 },
    { "p_name": "Lenora", "use_openings_book": True, "max_depth": 6,
        "judgement": 65, "vision": 65, "capture_score_base": 350 },
    { "p_name": "Killer", "use_openings_book": True, "max_depth": 6,
        "judgement": 100, "vision": 100, "capture_score_base": 300 },
    { "p_name": "Kelvin", "use_openings_book": True, "max_depth": 6,
        "judgement": 60, "vision": 60, "capture_score_base": 350 },
    { "p_name": "Jamima", "use_openings_book": True, "max_depth": 5,
        "judgement": 55, "vision": 55, "capture_score_base": 350 },
    { "p_name": "Irwin", "use_openings_book": True, "max_depth": 5,
        "judgement": 50, "vision": 50, "capture_score_base": 350 },
    { "p_name": "Henrietta", "use_openings_book": True, "max_depth": 4,
        "judgement": 45, "vision": 45, "capture_score_base": 350 },
    { "p_name": "Grant", "use_openings_book": True, "max_depth": 4,
        "judgement": 40, "vision": 40, "capture_score_base": 350 },
    { "p_name": "Fleur", "use_openings_book": False, "max_depth": 3,
        "judgement": 35, "vision": 35, "capture_score_base": 350 },
    { "p_name": "Erik", "use_openings_book": False, "max_depth": 3,
        "judgement": 30, "vision": 30, "capture_score_base": 350 },
    { "p_name": "Denise", "use_openings_book": False, "max_depth": 2,
        "judgement": 25, "vision": 25, "capture_score_base": 300 },
    { "p_name": "Claude", "use_openings_book": False, "max_depth": 2,
        "judgement": 20, "vision": 20, "capture_score_base": 400 },
    { "p_name": "Beatrice", "use_openings_book": False, "max_depth": 1,
        "judgement": 15, "vision": 15, "capture_score_base": 200 },
    { "p_name": "Anthony", "use_openings_book": False, "max_depth": 1,
        "judgement": 10, "vision": 10, "capture_score_base": 300 },
    { "p_name": "Tony", "use_openings_book": False, "max_depth": 1,
        "judgement": 0, "vision": 10, "capture_score_base": 400 },
    ]
    '''
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
    '''
    for p in players:
        genome.__dict__.update(p)
        dot()
        p = pm.find_by_name(genome.p_name, "Computer")
        if p:
            genome.p_key = p.p_key
        else:
            genome.p_key = pm.next_id()

        pm.save(genome.clone())

