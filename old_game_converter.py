#!/usr/bin/python

import game
import games_mgr as gm_m
import sys

def convert_file(filename, gm):
    game_list = open(filename).readlines()
    game_str = "".join(game_list)
    g = gm.create_game()
    g.load_game(game_str)
    gm.save(g)

if __name__ == "__main__":
    gm = gm_m.GamesMgr()

    for fn in sys.argv[1:]:
        convert_file(fn, gm)

