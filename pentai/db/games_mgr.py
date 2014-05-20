import pentai.base.game as g_m
import players_mgr
import preserved_game as pg_m
import zodb_dict as zd_m
import os
import pentai.base.gs_observer as gso_m

from pentai.base.defines import *

class GamesMgr(gso_m.GSObserver):
    # TODO: Borg pattern?
    def __init__(self, *args, **kwargs):
        self.games_dbs = {}
        self.players_mgr = players_mgr.PlayersMgr()
        id_section = "id_map"
        self.id_lookup = zd_m.get_section(id_section)
        u_s = "unfinished"
        self.unfinished_db = zd_m.get_section(u_s)

    def get_filename(self, key):
        if key.__class__ is g_m.Game:
            rk = key.rules.key()
        elif key.__class__ is tuple:
            rk = key[0]
        elif key.__class__ is int and key > 1000000:
            # Test for key >= very large number?
            # -> is from Openings DB
            rk = [19,'s']
        else:
            try:
                rk = self.id_lookup[key]
            except KeyError:
                return None

        fn = "%s_%s" % (rk[1], rk[0])
        return fn

    def ensure_has_id(self, game):
        assert not game is None
        if not hasattr(game, "game_id") or game.game_id is None:
            game_id = self.next_id()
            game.game_id = game_id

        return game.game_id

    def remove_id(self, key):
        if key is None:
            return None
        del self.id_lookup[key]
        zd_m.sync()

    def delete_game(self, key):
        game_db = self.get_db(key)
        if game_db is None:
            # No such game
            print "No such game: %s" % key
            return
        
        try:
            del game_db[key]
        except KeyError:
            # Corrupt DB, ignore
            print "No such game: %s" % key
            pass

        try:
            del self.unfinished_db[key]
        except KeyError:
            print "game not in unfinished_db: %s" % key
            print type(key)
            pass

        try:
            del self.id_lookup[key]
        except KeyError:
            print "game not in id_lookup: %s" % key
            print key
            pass
        zd_m.sync()

    def get_db(self, key):
        if key is None:
            return None
        
        fn = self.get_filename(key)
        if fn is None:
            return None

        try:
            f = self.games_dbs[fn]
        except KeyError:
            f = self.games_dbs[fn] = \
                zd_m.get_section(fn)
        return f

    def next_id(self):
        try:
            curr_id = self.id_lookup["id"]
        except KeyError:
            curr_id = 0
        curr_id += 1
        self.id_lookup["id"] = curr_id

        # Don't need to sync until it's saved
        return curr_id

    def create_game(self, rules=None, p1=None, p2=None):
        g = g_m.Game(rules, p1, p2)
        uid = self.next_id()
        g.game_id = uid
        if not rules is None:
            # Might as well save it now.
            self.id_lookup[uid] = rules.key()

        return g

    def save(self, g, game_db=None, update_cache=True):
        for p in g.get_all_players()[1:]:
            self.players_mgr.ensure_has_key(p)

        if game_db is None:
            game_db = self.get_db(g)
        
        self.ensure_has_id(g)
        pg = pg_m.PreservedGame(g)
        game_db[pg.key()] = pg

        self.id_lookup[g.game_id] = g.rules.key()
        zd_m.sync()

        gid = g.key()

        if g.finished():
            try:
                del self.unfinished_db[gid]
            except KeyError:
                pass
        else:
            self.unfinished_db[gid] = gid
        zd_m.sync()

        # Save players
        self.players_mgr.save(g.get_player(1), update_cache)
        self.players_mgr.save(g.get_player(2), update_cache)

    def sync_all(self):
        zd_m.sync()

    def get_unfinished_game(self, g_id):
        if not g_id in self.unfinished_db:
            return None
        return self.get_game(g_id)

    def get_all_unfinished(self):
        ret = []
        for g_id in self.unfinished_db.iterkeys():
            print "get_all_unfinished: %s" % g_id
            g = self.get_game(g_id, update_cache=False)
            ret.append(g)
        return ret

    def get_game(self, g_id, game_db=None, update_cache=True):
        pg = self.get_preserved_game(g_id, game_db, update_cache)

        if pg is None:
            return None

        g = pg.restore(self.players_mgr, update_cache)

        return g

    def get_preserved_game(self, g_id, game_db=None, update_cache=True):

        if g_id is None:
            return None

        if game_db is None:
            game_db = self.get_db(g_id)
            if game_db is None:
                return None

        try:
            pg = game_db[g_id]
        except KeyError:
            return None

        return pg
        
    def reset_state(self, game):
        pass

    def after_game_won(self, game, colour):
        # TODO: Check draws trigger this.
        self.save(game)

