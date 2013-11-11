
# This is just be a base class / interface to be filled out by 
# human and AI players.

# TODO: Undo
# TODO: Resign

class Player():
    """ Interface only """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def prompt_for_action(self, game, gui):
        pass

    def get_action(self, game, gui):
        pass

