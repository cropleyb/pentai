from player import *

# TODO: Split into another file
class AIPlayer(Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """
    def prompt_for_action(self, gui):
        # TODO: set up and execute AB search
        # gui.game
        ab_game = ABGame(gui.game)

        # pdb.set_trace()

        alpha_beta.alphabeta_search(ab_game.current_state, ab_game, max_depth=1)

    def get_action(self, gui):
        # TODO: make move chosen by the search
        return gui.get_action()
