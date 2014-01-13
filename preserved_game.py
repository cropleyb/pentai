from persistent_dict import *

class PreservedGame():
    def __init__(self, game):
        self.rules = game.rules # .clone?

        self.player = [None, game.player[1].key(), game.player[2].key()]

        self.move_history = game.move_history[:]

    def key(self):
        return "Freddo" # TODO

