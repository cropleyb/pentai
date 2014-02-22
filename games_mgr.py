import game
import players_mgr
import preserved_game as pg_m
import persistent_dict as pd_m
import os
import gs_observer as gso_m

from defines import *

class GamesMgr(gso_m.GSObserver):
    # TODO: Borg pattern?
    def __init__(self, prefix=None, *args, **kwargs):
        self.games_dbs = {}
        if prefix is None:
            prefix = os.path.join("db","")
        self.prefix = prefix
        self.players_mgr = players_mgr.PlayersMgr(prefix=prefix[:])
        id_filename = "%sid_map.pkl" % prefix
        self.id_lookup = pd_m.PersistentDict(id_filename)
        u_f = "%sunfinished.pkl" % prefix
        self.unfinished_db = pd_m.PersistentDict(u_f)

    def get_filename(self, key):
        if key.__class__ is game.Game:
            rk = key.rules.key()
        elif key.__class__ is tuple:
            rk = key[0]
        else:
            try:
                rk = self.id_lookup[key]
            except KeyError:
                return None

        fn = "%s%s_%s.pkl" % (self.prefix, rk[1], rk[0])
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
        self.id_lookup.sync()

    def delete_game(self, key):
        game_db = self.get_db(key)
        if game_db is None:
            # No such game
            return
        
        del game_db[key]
        game_db.sync()

        try:
            del self.unfinished_db[key]
            self.unfinished_db.sync()
        except KeyError:
            pass

        try:
            del self.id_lookup[key]
            self.id_lookup.sync()
        except KeyError:
            pass

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
                pd_m.PersistentDict(fn)
        return f

    def next_id(self):
        try:
            curr_id = self.id_lookup["id"]
        except KeyError:
            curr_id = 0
        curr_id += 1
        self.id_lookup["id"] = curr_id
        self.id_lookup.sync()
        return curr_id

    def create_game(self, rules=None, p1=None, p2=None):
        g = game.Game(rules, p1, p2)
        uid = self.next_id()
        g.game_id = uid
        if not rules is None:
            # Might as well save it now.
            self.id_lookup[uid] = rules.key()
            self.id_lookup.sync()

            # And save it to the DB when the game is finished
            if not self.prefix: # TODO: Make this a boolean self.test
                g.current_state.add_observer(self)

            # TODO: Save the game to game_db now?
        return g

    def save(self, g, game_db=None):
        for p in g.get_all_players()[1:]:
            self.players_mgr.ensure_has_key(p)

        if game_db is None:
            game_db = self.get_db(g)
        
        self.ensure_has_id(g)
        pg = pg_m.PreservedGame(g)
        game_db[pg.key()] = pg
        game_db.sync()

        self.id_lookup[g.game_id] = g.rules.key()
        self.id_lookup.sync()

        gid = g.get_game_id()

        if g.finished():
            try:
                del self.unfinished_db[gid]
            except KeyError:
                pass
        else:
            self.unfinished_db[gid] = gid
        self.unfinished_db.sync()

        # Save players
        self.players_mgr.save(g.get_player(1))
        self.players_mgr.save(g.get_player(2))

    def sync_all(self):
        self.unfinished_db.sync()
        self.id_lookup.sync()
        for g_db in self.games_dbs.itervalues():
            g_db.sync()
        self.players_mgr.sync()
        # TODO: Openings DB?

    def get_unfinished_game(self, g_id):
        if not g_id in self.unfinished_db:
            return None
        return self.get_game(g_id)

    def get_all_unfinished(self):
        ret = []
        for g_id in self.unfinished_db.iterkeys():
            g = self.get_game(g_id, update_cache=False)
            ret.append(g)
        return ret

    '''
    def get_recently_finished(self):
    '''

    def get_game(self, g_id, game_db=None, update_cache=True):
        if g_id is None:
            return None

        if game_db is None:
            game_db = self.get_db(g_id)
            if game_db is None:
                return None

        pg = game_db[g_id]
        if pg is None:
            return None

        g = pg.restore(self.players_mgr, update_cache)

        # Observe game
        g.current_state.add_observer(self)

        return g

    def reset_state(self, game):
        pass

    def after_game_won(self, game, colour):
        # TODO: Check draws trigger this.
        self.save(game)

