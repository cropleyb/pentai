
import game
import standardise
import persistent_dict as pd_m
import os
from defines import *
import preserved_game as pg_m
from pente_exceptions import *

instance = None

class OpeningsBook(object):
    def __init__(self, games_mgr, prefix=None):
        self.games_mgr = games_mgr
        self.positions_dbs = {}
        if prefix is None:
            prefix = os.path.join("db","")
        self.prefix = prefix

        global instance
        instance = self

    def get_filename(self, g):
        if g.__class__ is game.Game:
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
            f = self.positions_dbs[fn] = pd_m.PersistentDict(fn)
        return f

    def add_game(self, g, db=None):
        # Save the game first, before it is manipulated
        self.games_mgr.save(g)

        # Copy the game instance as this process munges the game.
        pm = self.games_mgr.players_mgr
        g = pg_m.PreservedGame(g).restore(pm)

        if not g.finished():
            # Only add finished games to the openings book
            return

        # Set the game as unfinished to game_state from raising exceptions
        # when we try to replay the game?! (TODO: Why is this special?)
        g.current_state._won_by = EMPTY

        for mn in range(1, 1+len(g.move_history)):
            # Only needs to be looked up the first time
            db = self.add_position(g, mn, db)
        db.sync()

    def add_position(self, game, move_number, db=None, sync=False):
        game.go_to_move(move_number)

        std_state, fwd, rev = standardise.standardise(game.current_state)
        position_key = (tuple(std_state.board.strips[0].strips),
                game.get_captured(BLACK),
                game.get_captured(WHITE))

        # Get the appropriate file for positions of this rule type and size
        if db is None:
            db = self.get_db(game)
        pos_slot = db.setdefault(position_key, {})
        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        assert(standardised_move[0] >= 0)
        assert(standardised_move[1] >= 0)
        arr = pos_slot.setdefault(standardised_move, [])
        if move_number == 1:
            # Should only be in there once per id
            if game.game_id in arr:
                raise OpeningsBookDuplicateException()
        arr.append(game.game_id)

        if sync:
            db.sync()
            self.games_mgr.save(game)
        return db

    def get_move_games(self, game):
        std_state, fwd, rev = standardise.standardise(game.current_state)

        position_key = (tuple(std_state.board.strips[0].strips),
                              game.get_captured(BLACK),
                              game.get_captured(WHITE))

        db = self.get_db(game)

        options = {}
        try:
            pos_slot = db[position_key]
            size = game.size()
            for pos, gids in pos_slot.iteritems():
                x, y = rev(*pos)
                if x < 0: x += size - 1
                if y < 0: y += size - 1

                # Convert the game_ids to games
                for gid in gids:
                    g = self.games_mgr.get_game(gid, update_cache=False)
                    if g:
                        options.setdefault((x,y),[]).append(g)
        except KeyError:
            return
        for move, games in options.iteritems():
            yield move, games

    def after_game_won(self, game, colour):
        # Add the game to the openings library if req.
        # (i.e. we're subscribed)
        self.add_game(game)

