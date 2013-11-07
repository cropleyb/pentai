
# TODO: This should just be a base class / interface to be filled out by 
# human and AI players.

# Action types:
# Move
# TODO: Undo
# TODO: Resign



class Player():
    """ Interface only """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def prompt_for_action(self, gui):
        pass

    def get_action(self, gui):
        pass

# TODO: Split into another file
class HumanPlayer(Player):
    def prompt_for_action(self, gui):
        return gui.request_move(self.name)

    def get_action(self, gui):
        return gui.get_action()

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
