from base_db import *

import game
from preserved_game import *
from base_db import *
from players_mgr import *

from persistent_dict import *

class GamesMgr(object):
    # TODO: Borg pattern?
    def __init__(self, prefix=None, *args, **kwargs):
        self.games_dbs = {}
        if prefix is None:
            prefix = os.path.join("db","")
        self.prefix = prefix

        self.players_mgr = PlayersMgr(prefix=prefix)
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
            f = self.games_dbs[fn] = \
                PersistentDict(fn, 'c', format='pickle')
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
        self.id_lookup.sync()
        return g

    def save(self, g, game_db=None):
        if game_db is None:
            game_db = self.get_db(g)
        
        pg = PreservedGame(g)
        game_db[pg.key()] = pg
        game_db.sync()
        gid = g.get_game_id()

        if g.finished():
            try:
                del self.unfinished_db[gid]
            except KeyError:
                pass
        else:
            self.unfinished_db[gid] = gid
        self.unfinished_db.sync()

    def get_unfinished_game(self, g_id):
        if not g_id in self.unfinished_db:
            return None
        return self.get_game(g_id)

    def get_game(self, g_id, game_db=None):
        if g_id is None:
            return None

        if game_db is None:
            game_db = self.get_db(g_id)

        pg = game_db[g_id]
        if pg is None:
            return None

        g = pg.restore(self.players_mgr)
        return g
