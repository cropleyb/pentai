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

    def reincarnate(self, ai_db):
        orig_game = Game()
        orig_game.rules = Rules(*self.rules)
        orig_game.date = self.date
        orig_game.winner = self.winner
        orig_game.move_history = self.moves[:]
        orig_game.players = [ai_db.find(p) for p in self.players]

        return orig_game
