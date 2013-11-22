import ab_bridge
import alpha_beta
from gui import *

from player import *

import threading

class AIPlayer(Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, max_depth, *args, **vargs):
        Player.__init__(self, *args, **vargs)
        self.max_depth = max_depth
        '''
        #TODO use super?
        def __init__(self, max_depth, *args, **kwargs):
            super(AIPlayer, self).__init__(*args, **kwargs)
        '''

    def attach_to_game(self, base_game):
        self.ab_game = ab_bridge.ABGame(base_game)

    def prompt_for_action(self, base_game, gui):
        t = threading.Thread(target=self.search_thread, args=(gui,))
        t.daemon = False
        t.start()
        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "computer"

    def search_thread(self, gui):
        ab_game = self.ab_game
        move, value = alpha_beta.alphabeta_search(ab_game.current_state, ab_game,
                max_depth=self.max_depth)
        action = move[0]
        gui.enqueue_action(action)
        gui.trig()

