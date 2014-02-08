from player import *

class HumanPlayer(Player):
    def prompt_for_action(self, game, gui):
        return gui.request_move(self.p_name)

    def get_action(self, game, gui):
        return gui.get_action()

    def get_type(self):
        return "Human"

    def set_interrupted(self):
        pass
