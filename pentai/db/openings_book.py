import os

from pentai.base.defines import *
from pentai.base.pente_exceptions import *
import pentai.base.game as g_m
import pentai.db.zodb_dict as z_m
import pentai.ai.standardise as st_m
import pentai.db.preserved_game as pg_m
import pentai.db.openings_builder as obl_m

ZM = z_m.ZM
ZL = z_m.ZL

instance = None

class OpeningsBook(object):
    def __init__(self, games_mgr):
        self.games_mgr = games_mgr
        self.positions_dbs = ZM()

        global instance
        instance = self

    def add_openings(self):
        obl_m.build(self)

    def get_filename(self, g):
        return "move%s" % g.get_move_number()

    def get_db(self, g):
        if g is None:
            return None
        fn = self.get_filename(g)
        try:
            f = self.positions_dbs[fn]
        except KeyError:
            f = self.positions_dbs[fn] = z_m.get_section(fn)
        return f

    def add_game(self, g):
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
            self.add_position(g, mn)
        z_m.sync()

    def add_position(self, game, move_number, db=None, sync=False):
        game.go_to_move(move_number)

        std_state, fwd, rev = st_m.standardise(game.current_state)
        position_key = std_state
        #print "Add: %s" % (std_state,)

        # Get the appropriate section for positions of this rule type and size
        db = self.get_db(game)
        pos_slot = db.setdefault(position_key, ZM())
        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        assert(standardised_move[0] >= 0)
        assert(standardised_move[1] >= 0)
        arr = pos_slot.setdefault(standardised_move, ZL())
        if move_number == 1:
            # Should only be in there once per id
            if game.game_id in arr:
                raise OpeningsBookDuplicateException()
        arr.append(game.game_id)

        if sync:
            self.games_mgr.save(game)
            z_m.sync()
        return db

    def get_move_games(self, game):
        std_state, fwd, rev = st_m.standardise(game.current_state)
        #print "Get: %s" % (std_state,)

        position_key = std_state

        db = self.get_db(game)

        options = {}
        try:
            # TODO
            pos_slot = db[position_key]
            size = game.size()
            for pos, gids in pos_slot.iteritems():
                x, y = rev(*pos)
                if x < 0: x += size - 1
                if y < 0: y += size - 1

                # Convert the game_ids to games
                for gid in gids:
                    g = self.games_mgr.get_preserved_game(gid, update_cache=False)
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

