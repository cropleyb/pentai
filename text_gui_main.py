#!/usr/bin/python

import alpha_beta
import ab_bridge
from rules import *
from game import *
from text_gui import *
from player import *

# txt_gui_main.py creates the Game, Players and contains the game turn loop



if __name__ == "__main__":
    """
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"
    """

    rules = Rules(7, "standard")
    player1 = HumanPlayer("Bruce")
    player2 = HumanPlayer("B2")
    game = Game(rules, player1, player2)

    gui = TextGui(game)

    while (True):
        if game.get_move_number() % 2 == 0:
            p = player1
        else:
            p = player2
        print p.prompt_for_action(gui)
        action = p.get_action(gui)
        game.perform(action)

    #pdb.set_trace()
    # alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
