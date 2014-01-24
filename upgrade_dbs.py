#!/usr/bin/python

import games_mgr as gm_m
import openings_book as ol_m
import player as p_m
from defines import *

import pdb

if __name__ == "__main__":
    gm = gm_m.GamesMgr()
    #pdb.set_trace()
    
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

    for g_id in to_remove:
        gm.remove_id(g_id)
