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
        if not hasattr(player, "p_key") or player.p_key is None:
            p_key = self.next_id()
            player.p_key = p_key

        return player.p_key

    def get_player_names(self):
        l = [ g.get_name() for k,g in self.players.iteritems()
                if (k != "max_id") and
                   (g.__class__ == ai_genome.AIGenome) ]
        return l

    def remove(self, pid):
        del self.players[pid]

    def save(self, player):
        if player.__class__ is type(0):
            player = self.find(player)

        p_key = self.ensure_has_key(player)

        try:
            player = player.genome
            # update the genome as well
            player.set_override(True)
            player.p_key = p_key
            player.set_override(False)
        except AttributeError:
            # We're already dealing with a genome
            pass

        self.players[p_key] = player
        self.players.sync()

    def sync(self):
        self.players.sync()

    def find_by_name(self, name):
        for p_key, genome in self.players.iteritems():
            if genome.p_name == name:
                return self.find(p_key)

    def find_genome_by_name(self, name):
        for p_key, genome in self.players.iteritems():
            if genome.__class__ != ai_genome.AIGenome:
                continue
            if genome.p_name == name:
                return genome

    def find(self, p_key):
        try:
            p = self.players[p_key]
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

