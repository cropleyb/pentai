import ab_game
import alpha_beta
from gui import *

from player import *

import threading

class AIPlayer(Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, *args, **vargs):
        Player.__init__(self, *args, **vargs)
        self.max_depth = 1

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth

    def attach_to_game(self, base_game):
        self.ab_game = ab_game.ABGame(base_game)

    def prompt_for_action(self, base_game, gui, test=False):
        if test:
            return self.do_the_search()
        else:
            t = threading.Thread(target=self.search_thread, args=(gui,))

            # Allow the program to be exited quickly
            t.daemon = True

            t.start()
        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "computer"

    def search_thread(self, gui):
        action = self.do_the_search()
        gui.enqueue_action(action)
        gui.trig()

    def do_the_search(self):
        ab_game = self.ab_game
        md = self.max_depth
        '''
        if ab_game.current_state.get_move_number() < 10:
            md = min(md, 4)
        '''
        print "%s. " % ab_game.current_state.get_move_number(),
        print ab_game.current_state.utility_stats,
        move, value = alpha_beta.alphabeta_search(ab_game.current_state,
                ab_game, max_depth=md)
        action = move[0]
        print " => %s" % (action,)
        return action

