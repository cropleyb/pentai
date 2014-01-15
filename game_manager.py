from base_db import *

import game
import preserved_game
import games_db

from players_mgr import *
from persistent_dict import *

class GameManager(object):
    def __init__(self, pdb_filename, gm_filename, test_prefix="", *args, **kwargs):
        self.files = {}
        self.player_mgr = PlayersMgr(pdb_filename)
        self.test_prefix = test_prefix
        self.data = PersistentDict(gm_filename, 'c', format='pickle')
        self.recent_db = games_db.GamesDB("%srecent.pkl" % test_prefix)

    def get_filename(self, g):
        if g.__class__ is game.Game:
            rk = g.rules.key()
        elif g.__class__ is tuple:
            rk = g[0]
        else:
            rk = g

        fn = "%s%s_%s.pkl" % (self.test_prefix, rk[1], rk[0])
        return fn

    def get_db(self, g):
        if g is None:
            return None
        fn = self.get_filename(g)
        try:
            f = self.files[fn]
        except KeyError:
            f = self.files[fn] = games_db.GamesDB(fn)
        return f

    def next_id(self):
        try:
            curr_id = self.data["id"]
        except KeyError:
            curr_id = 0
        curr_id += 1
        self.data["id"] = curr_id
        self.data.sync()
        return curr_id

    def create_game(self, rules, p1, p2):
        g = game.Game(rules, p1, p2)
        uid = self.next_id()
        g.game_id = rules.key(), uid
        return g

    def save(self, g, game_db=None):
        if game_db is None:
            game_db = self.get_db(g)
        
        pg = preserved_game.PreservedGame(g)
        game_db.add(pg)
        if g.finished():
            self.recent_db.remove(g.get_game_id())
        else:
            self.recent_db.add(pg)

    def get_game_from_db(self, g_id, game_db):
        if g_id is None:
            return None

        pg = game_db.find(g_id)
        if pg is None:
            return None
        g = pg.restore(self.player_mgr)
        return g
    
    def get_recent_game(self, g_id):
        return self.get_game_from_db(g_id, self.recent_db)

    def get_game(self, g_id):
        if g_id is None:
            return None

        game_db = self.get_db(g_id)

        return self.get_game_from_db(g_id, game_db)

    def get_game_from_db(self, g_id, game_db):
        pg = game_db.find(g_id)
        if pg is None:
            return None
        g = pg.restore(self.player_mgr)
        return g
        
