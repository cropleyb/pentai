#!/usr/bin/python

import alpha_beta
import ab_bridge

# txtGuiMain.py creates the Game, Players and contains the game turn loop


if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    g = Game(7)

    #pdb.set_trace()
    alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
