import ai_factory
import ai_genome
import persistent_dict
import os

from defines import *

class PlayersMgr():
    # TODO: Borg pattern?
    def __init__(self, prefix=None, *args, **kwargs):
        self.factory = ai_factory.AIFactory()
        if prefix is None:
            prefix = os.path.join("db","")
        filename = "%splayers.pkl" % prefix
        self.players = persistent_dict.PersistentDict(filename)

    def ensure_has_key(self, player):
        assert not player is None
        if not hasattr(player, "key") or player.key is None:
            key = self.next_id()
            player.key = key

        return player.key

    def get_player_names(self):
        l = [ g.name for k,g in self.players.iteritems()
                if (k != "max_id") and
                   (g.__class__ == ai_genome.AIGenome) ]
        return l

    def remove(self, pid):
        del self.players[pid]

    def save(self, player):
        if player.__class__ is type(0):
            player = self.find(player)

        key = self.ensure_has_key(player)

        try:
            player = player.genome
            # update the genome as well
            player.key = key
        except AttributeError:
            # We're already dealing with a genome
            pass

        self.players[key] = player
        self.players.sync()

    def sync(self):
        self.players.sync()

    def find_by_name(self, name):
        for key, genome in self.players.iteritems():
            if genome.name == name:
                return self.find(key)

    def find_genome_by_name(self, name):
        for key, genome in self.players.iteritems():
            if genome.__class__ != ai_genome.AIGenome:
                continue
            if genome.name == name:
                return genome


    def find(self, key):
        try:
            p = self.players[key]
        except KeyError:
            return None
        if p.__class__ is ai_genome.AIGenome:
            p = self.factory.create_player(p)
        else:
            # HumanPlayers are stored directly
            pass
        return p

    def next_id(self):
        try:
            curr_id = self.players["max_id"]
        except KeyError:
            curr_id = 0
        curr_id += 1
        self.players["max_id"] = curr_id
        self.players.sync()
        return curr_id

