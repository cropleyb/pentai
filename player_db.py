import base_db
from ai_factory import *

class PlayerDB(base_db.BaseDB):
    def __init__(self, *args, **kwargs):
        self.factory = AIFactory()
        super(PlayerDB, self).__init__(*args, **kwargs)

    def add(self, player):
        try:
            player = player.genome
        except AttributeError:
            pass
        super(PlayerDB, self).add(player)

    def find(self, key):
        try:
            g = self.objs[key]
        except KeyError:
            return None
        if g.__class__ is Genome:
            p = self.factory.create_player(g)
        else:
            # HumanPlayer is stored directly
            p = g
        return p

