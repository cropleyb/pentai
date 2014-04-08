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

    # Map from player id to unique player id for that id (with unique name)
    dup_ids_map = {}

    # The id that will be used as the unique player id for a name
    seen_name_map = {}

    for p_id, genome in pm.players.iteritems():
        gn = genome.name
        if gn in seen_name_map:
            dup_ids_map[p_id] = seen_name_map[gn]
        else:
            seen_name_map[gn] = p_id

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
            pid = game.players[colour]
            if pid is None:
                pid = unknown
            else:
                try:
                    pid = dup_ids_map[pid]
                except:
                    # Already using the right one
                    pass
            game.players[colour] = pid
        gm.save(game)
        dot()

    print "Removing games"
    for g_id in to_remove:
        dot()
        gm.remove_id(g_id)

    print "Removing duplicate players"
    for dup, orig in dup_ids_map.items():
        pm.remove(dup)
    gm.sync_all()

    #sys.exit()

    # TODO upgrade openings

