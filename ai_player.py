import ab_bridge
import alpha_beta
from gui import *

from player import *

class AIPlayer(Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, name):
        #TODO fix hack
        Player.__init__(self, name)

        self.max_depth = 1

    def attach_to_game(self, base_game):
        self.ab_game = ab_bridge.ABGame(base_game)

    def prompt_for_action(self, base_game, gui):
        ab_game = self.ab_game
        move, value = alpha_beta.alphabeta_search(ab_game.current_state, ab_game,
                max_depth=self.max_depth)
        self.action = move[0]
        return self.action

    def get_action(self, game, gui):
        # TODO: make move chosen by the search
        return self.action
