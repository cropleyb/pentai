from player import *

class HumanPlayer(Player):
    def prompt_for_action(self, gui):
        return gui.request_move(self.name)

    def get_action(self, gui):
        return gui.get_action()

