
import pdb

from defines import *
from standardise import *
from persistent_dict import *

class OpeningsMgr(object):
    def __init__(self, prefix=None):
        self.games = {}
        if prefix is None:
            prefix = os.path.join("db","")
        pos_fn = "%spositions.pkl" % prefix # TODO: rules
        self.positions = PersistentDict(pos_fn)

    def get_games(self, rules):
        try:
            return self.games[rules]
        except KeyError:
            return []

    def add_game(self, g):
        rules = g.rules
        self.games.setdefault(rules, []).append(g)

        for mn in range(1, 1+len(g.move_history)):
            self.add_position(g, mn)

    def add_position(self, game, move_number, sync=False):
        game.go_to_move(move_number)

        std_state, fwd, rev = standardise(game.current_state)
        position_key = (tuple(std_state.board.strips[0].strips), game.get_captured(BLACK),
                    game.get_captured(WHITE))

        position_slot = self.positions.setdefault(position_key, [])
        next_move = game.move_history[move_number-1]
        position_slot.append((fwd(*next_move), game))

        if sync:
            self.positions.sync()

    def get_moves(self, game):
        std_state, fwd, rev = standardise(game.current_state)
        position_key = (tuple(std_state.board.strips[0].strips), game.get_captured(BLACK),
                    game.get_captured(WHITE))

        try:
            position_slot = self.positions[position_key]
            size = game.size()
            for pos, game in position_slot:
                x, y = rev(*pos)
                if x < 0: x += size - 1
                if y < 0: y += size - 1
                yield (x,y), game
        except KeyError:
            return

