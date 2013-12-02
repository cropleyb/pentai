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
            self.search_thread(gui, True)
        else:
            t = threading.Thread(target=self.search_thread, args=(gui,))

            # Allow the program to be exited quickly
            t.daemon = True

            t.start()
        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "computer"

    def search_thread(self, gui, test=False):
        ab_game = self.ab_game
        move, value = alpha_beta.alphabeta_search(ab_game.current_state, ab_game,
                max_depth=self.max_depth)
        action = move[0]
        if test:
            self.action = action
        else:
            gui.enqueue_action(action)
            gui.trig()

    # TODO This is only for testing!
    def get_action(self, game, gui):
        return self.action

