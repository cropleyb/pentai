from base_db import *

import game
from preserved_game import *
from base_db import *

from persistent_dict import *

class GamesMgr(object):
    def __init__(self, players_mgr, prefix=None, *args, **kwargs):
        self.games_dbs = {}
        self.player_mgr = players_mgr
        if prefix is None:
            prefix = os.path.join("db","")
        self.prefix = prefix
        id_filename = "%sid_map.pkl" % prefix
        self.id_lookup = PersistentDict(id_filename, 'c', format='pickle')
        self.unfinished_db = PersistentDict("%sunfinished.pkl" % prefix, 'c', format='pickle')

    def get_filename(self, key):
        if key.__class__ is game.Game:
            rk = key.rules.key()
        elif key.__class__ is tuple:
            rk = key[0]
        else:
            rk = self.id_lookup[key]

        fn = "%s%s_%s.pkl" % (self.prefix, rk[1], rk[0])
        return fn

    def get_db(self, key):
        if key is None:
            return None
        fn = self.get_filename(key)
        try:
            f = self.games_dbs[fn]
        except KeyError:
            f = self.games_dbs[fn] = BaseDB(fn)
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

    def create_game(self, rules, p1, p2):
        g = game.Game(rules, p1, p2)
        uid = self.next_id()
        g.game_id = uid
        self.id_lookup[uid] = rules.key()
        return g

    def save(self, g, game_db=None):
        if game_db is None:
            game_db = self.get_db(g)
        
        pg = PreservedGame(g)
        game_db.add(pg)
        gid = g.get_game_id()

        if g.finished():
            try:
                del self.unfinished_db[gid]
            except KeyError:
                pass
        else:
            self.unfinished_db[gid] = gid

    def get_unfinished_game(self, g_id):
        try:
            g_id = self.unfinished_db[g_id]
            db = self.get_db(g_id)
            return self.get_game_from_db(g_id, db)
        except KeyError:
            return None

    def get_game(self, g_id):
        if g_id is None:
            return None

        game_db = self.get_db(g_id)

        return self.get_game_from_db(g_id, game_db)

    def get_game_from_db(self, g_id, game_db):
        if g_id is None:
            return None

        pg = game_db.find(g_id)
        if pg is None:
            return None
        g = pg.restore(self.player_mgr)
        return g
