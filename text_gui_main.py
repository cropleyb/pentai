#!/usr/bin/python

import alpha_beta
import ab_bridge
from rules import *
from game import *
from text_gui import *
from player import *

import pdb
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
    # HACK
    game.current_state.gui = gui

    while (not game.finished()):
        print game.prompt_for_action(gui),
        #pdb.set_trace()
        try:
            action = game.get_action(gui)
            action.perform(game)
        except IllegalMoveException:
            print "sorry that isn't a legal move"
    # alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
