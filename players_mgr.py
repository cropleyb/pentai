from ai_factory import *

class PlayersMgr():
    # TODO: Borg pattern?
    def __init__(self, prefix=None, *args, **kwargs):
        self.factory = AIFactory()
        if prefix is None:
            prefix = os.path.join("db","")
        filename = "%splayers.pkl" % prefix
        self.players = PersistentDict(filename, 'c', format='pickle')

    def add(self, player):
        try:
            player = player.genome
        except AttributeError:
            pass
        self.players[player.key()] = player
        self.players.sync()

    def find(self, key):
        try:
            g = self.players[key]
        except KeyError:
            return None
        if g.__class__ is Genome:
            p = self.factory.create_player(g)
        else:
            # HumanPlayers are stored directly
            p = g
        return p

