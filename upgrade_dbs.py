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

if __name__ == "__main__":
    print "Upgrading Players"
    pm = pm_m.PlayersMgr()
    for p_id, genome in pm.players.iteritems():
        if p_id == "max_id":
            continue
        sys.stdout.write('.')
        dot()
        pm.save(genome)

    print "Upgrading Games"
    gm = gm_m.GamesMgr()
    to_remove = []
    unknown = p_m.Player("Unknown")

    for g_id in gm.id_lookup.iterkeys():
        if g_id == "id":
            continue
        try:
            game = gm.get_game(g_id)
        except KeyError:
            print "Removing game %s" % g_id
            to_remove.append(g_id)
            continue
        for colour in (BLACK,WHITE):
            if game.players[colour] is None:
                game.players[colour] = unknown
        gm.save(game)
        dot()

    for g_id in to_remove:
        dot()
        gm.remove_id(g_id)

    # TODO upgrade openings

