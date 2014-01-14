from base_db import *

import game
import preserved_game
import games_db
from player_db import *

class GameManager(BaseDB):
    def __init__(self, pdb_filename, *args, **kwargs):
        self.files = {}
        self.player_db = PlayerDB(pdb_filename)

        super(GameManager, self).__init__(*args, **kwargs)

    def get_filename(self, g):
        if g.__class__ is game.Game:
            rk = g.rules.key()
        elif g.__class__ is tuple:
            rk = g[0]
        else:
            rk = g

        fn = "%s_%s.pkl" % (rk[1], rk[0])
        return fn

    def get_file(self, g):
        fn = self.get_filename(g)
        try:
            f = self.files[fn]
        except KeyError:
            f = self.files[fn] = games_db.GamesDB(fn)
        return f

    def create_game(self, rules, p1, p2):
        g = game.Game(rules, p1, p2)
        uid = 1 # TODO
        g.game_id = rules.key(), uid
        return g

    def save(self, g):
        f = self.get_file(g)
        
        pg = preserved_game.PreservedGame(g)
        f.add(pg)

    def get_game(self, g_id):
        game_file = self.get_file(g_id)

        pg = game_file.find(g_id)
        if pg is None:
            return None
        g = pg.restore(self.player_db)
        return g
        
