from game import *
from persistent_dict import *

class PreservedGame():
    def __init__(self, game=None):
        if game:
            self.game_id = game.game_id
            self.rules = game.rules.key()
            self.date = game.get_date()
            self.players = [None,
                    game.get_player(1).get_key(),
                    game.get_player(2).get_key()]
            self.won_by = game.get_won_by()
            self.moves = game.move_history[:]
            self.resume_move_number = game.resume_move_number

    def key(self):
        return self.game_id

    def restore(self, pm, update_cache=True):
        p1 = pm.find(self.players[1], update_cache)
        p2 = pm.find(self.players[2], update_cache)
        orig_game = Game(rules.Rules(*self.rules), p1, p2)
        orig_game.game_id = self.game_id
        orig_game.date = self.date
        try:
            won_by = self.won_by
        except AttributeError:
            # Backward compatibility
            won_by = self.winner
        orig_game.set_won_by(won_by)
        orig_game.move_history = self.moves[:]
        try:
            orig_game.resume_move_number = self.resume_move_number
        except AttributeError:
            orig_game.resume_move_number = None

        return orig_game
