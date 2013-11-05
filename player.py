
# TODO: This should just be a base class / interface to be filled out by 
# human and AI players.

class Player():
    def __init__(self, name, gui):
        self.name = name

    def __repr__(self):
        return self.name

    def prompt_for_action(self):
        pass

    def get_action(self):
        pass

class HumanPlayer(Player):
    def prompt_for_action(self):
        gui.request_move(self.name)

    def get_action(self):
        pass
        # TODO: gui create and return an Action object
        # return gui.get_action()
