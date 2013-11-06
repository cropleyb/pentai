
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

    def prompt_for_action(self):
        pass

    def get_action(self):
        pass

# TODO: Split into another file
class HumanPlayer(Player):
    def prompt_for_action(self, gui):
        return gui.request_move(self.name)

    def get_action(self, gui):
        return gui.get_action()
