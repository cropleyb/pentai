
# This is just be a base class / interface to be filled out by 
# human and AI players.

# TODO: Undo support?
# TODO: Resign

class Player():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def get_key(self):
        return self.key

    def get_name(self):
        return self.name

    def prompt_for_action(self, game, gui):
        pass

    def get_action(self, game, gui):
        pass

    def rating_factor(self):
        return 1

    def attach_to_game(self, base_game):
        pass

