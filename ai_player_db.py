import base_db
import ai_factory

class AIPlayerDB(base_db.BaseDB):
    def __init__(self, *args, **kwargs):
        self.factory = ai_factory.AIFactory()
        super(AIPlayerDB, self).__init__(*args, **kwargs)

    def add(self, player):
        genome = player.genome
        super(AIPlayerDB, self).add(genome)

    def find(self, key):
        try:
            g = self.objs[key]
        except KeyError:
            return None
        p = self.factory.create_player(g)
        return p

