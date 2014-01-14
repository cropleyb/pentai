from game import *
from persistent_dict import *

class PreservedGame():
    def __init__(self, game=None):
        if game:
            self.rules = game.rules.key()
            self.date = game.get_date()
            self.players = [None, game.player[1].key(), game.player[2].key()]

            self.winner = game.winner()
            self.moves = game.move_history[:]

    def key(self):
        return "Freddo" # TODO

    def reincarnate(self):
        orig_game = Game()
        orig_game.rules = Rules(*self.rules)
        orig_game.date = self.date
        orig_game.winner = self.winner
        orig_game.move_history = self.moves[:]

        # TODO: reincarnate players from player db
        orig_game.players = self.players[:]
        #orig_game.players = [None, self.players[1].key(), self.players[2].key()]

        return orig_game
