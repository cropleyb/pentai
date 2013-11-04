#!/usr/bin/python

import alpha_beta
import ab_bridge
from rules import *
from game import *
from text_gui import *
from player import *

# txt_gui_main.py creates the Game, Players and contains the game turn loop



if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    rules = Rules(7, "standard")
    player1 = Player("Bruce")
    player2 = Player("B2")
    game = Game(rules, player1, player2)

    gui = TextGui(game)

    #pdb.set_trace()
    # alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
