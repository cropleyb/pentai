#!/usr/bin/python

import games_mgr as gm_m
import openings_book as ol_m
import player as p_m
import players_mgr as pm_m
from defines import *

import sys
import os

def dot():
    sys.stdout.write('.')
    sys.stdout.flush()

def check_id(g_id, to_remove):
    if g_id == "id":
        return

    game = None
    try:
        game = gm.get_game(g_id)
    except KeyError:
        pass
    if game is None:
        log.debug("Removing game %s" % g_id)
        to_remove.append(g_id)
    
    dot()

if __name__ == "__main__":
    log.debug("Cleaning Games")
    global gm
    gm = gm_m.GamesMgr()
    to_remove = []
    unknown = p_m.Player("Unknown")

    for g_id in gm.id_lookup.iterkeys():
        check_id(g_id, to_remove)

    for g_id in gm.unfinished_db.iterkeys():
        check_id(g_id, to_remove)

    for g_id in to_remove:
        dot()
        gm.delete_game(g_id)
        #gm.remove_id(g_id)

    gm.sync_all()

