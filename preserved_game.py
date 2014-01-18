from game import *
from persistent_dict import *

class PreservedGame():
    def __init__(self, game=None):
        if game:
            self.game_id = game.game_id
            self.rules = game.rules.key()
            self.date = game.get_date()
            self.players = [None, game.player[1].key(), game.player[2].key()]
            self.winner = game.winner()
            self.moves = game.move_history[:]

    def key(self):
        return self.game_id

    def restore(self, ai_db):
        p1 = ai_db.find(self.players[1])
        p2 = ai_db.find(self.players[2])
        orig_game = Game(rules.Rules(*self.rules), p1, p2)
        orig_game.game_id = self.game_id
        orig_game.date = self.date
        orig_game.set_won_by(self.winner)
        orig_game.move_history = self.moves[:]

        return orig_game
