
import pdb
from game import *
from defines import *
from standardise import *
from persistent_dict import *

class OpeningsMgr(object):
    def __init__(self, prefix=None):
        self.games = {}
        self.positions_dbs = {}
        if prefix is None:
            prefix = os.path.join("db","")
        self.prefix = prefix

    def get_filename(self, g):
        if g.__class__ is Game:
            rk = g.rules.key()
        elif g.__class__ is tuple:
            rk = g[0]
        else:
            rk = g

        fn = "%s%s_%s_openings.pkl" % (self.prefix, rk[1], rk[0])
        return fn

    def get_db(self, g):
        if g is None:
            return None
        fn = self.get_filename(g)
        try:
            f = self.positions_dbs[fn]
        except KeyError:
            f = self.positions_dbs[fn] = PersistentDict(fn)
        return f

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
        position_key = (tuple(std_state.board.strips[0].strips),
                game.get_captured(BLACK),
                game.get_captured(WHITE))

        # Get the appropriate file for positions of this rule type and size
        db = self.get_db(game)
        pos_slot = db.setdefault(position_key, {})
        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        arr = pos_slot.setdefault(standardised_move, [])
        arr.append(game)

        if sync:
            db.sync()

    def get_move_games(self, game):
        std_state, fwd, rev = standardise(game.current_state)

        position_key = (tuple(std_state.board.strips[0].strips),
                              game.get_captured(BLACK),
                              game.get_captured(WHITE))

        db = self.get_db(game)
        try:
            pos_slot = db[position_key]
            size = game.size()
            for pos, games in pos_slot.iteritems():
                x, y = rev(*pos)
                if x < 0: x += size - 1
                if y < 0: y += size - 1
                yield (x,y), games
        except KeyError:
            return

