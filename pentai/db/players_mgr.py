import pentai.ai.ai_genome as aig_m
import ai_factory
import misc_db as m_m
import mru_cache as mru_m

from pentai.base.defines import *
import pentai.base.logger as log
import zodb_dict as z_m

import os

def misc():
    return m_m.get_instance()

class PlayersMgr():
    # TODO: Borg pattern?
    def __init__(self, *args, **kwargs):
        self.factory = ai_factory.AIFactory()
        section = "players"
        self.players = z_m.get_section(section)

    def ensure_has_key(self, player):
        assert not player is None
        if not hasattr(player, "p_key") or player.p_key is None:
            p_key = self.next_id()
            player.p_key = p_key

        return player.p_key

    def get_rpks(self, player_type):
        if player_type == "Computer":
            key = "recent_ai_player_ids"
        else:
            key = "recent_human_ids"
        rpks = misc().setdefault(key, mru_m.MRUCache(30))
        return rpks

    def mark_recent_player(self, player):
        log.debug("in mark_recent_player")
        try:
            p_key = player.get_key()
        except AttributeError:
            p_key = player

        player = self.convert_to_player(p_key)
        p_type = player.get_type()
        rpks = self.get_rpks(p_type)
        rpks.add(p_key)
        z_m.sync()

    def get_recent_player_names(self, player_type, number):
        # TODO: use "number" for # returned players
        rps = self.get_recent_players(player_type, number)
        rpns = []
        seen = set()
        for rp in rps:
            rpn = rp.get_name()
            if not rpn in seen:
                rpns.append(rpn)
                seen.add(rpn)
        return rpns

    def get_ai_player_names(self):
        return self.get_recent_player_names("Computer", 30)

    def get_human_player_names(self):
        return self.get_recent_player_names("Human", 30)

    def get_recent_players(self, player_type, number):
        rpks = self.get_rpks(player_type).top(number)
        rps = []
        for rp in rpks:
            p = self.convert_to_player(rp)
            if p:
                rps.append(p)
        return rps

    def remove(self, pid):
        del self.players[pid]

    def save(self, player, update_cache=True):
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
        if update_cache:
            self.mark_recent_player(p_key)
        z_m.sync()

    def find_by_name(self, name, player_type=None, update_cache=True):
        genome = self.find_genome_by_name(name, player_type, update_cache)
        if genome:
            return self.convert_to_player(genome)

    def find_genome_by_name(self, name, player_type=None, update_cache=True):
        for p_key, genome in self.players.iteritems():
            if type(genome) == type(0):
                continue
            if player_type and genome.get_type() != player_type:
                continue
            if genome.get_name() == name:
                if update_cache:
                    self.mark_recent_player(p_key)
                return genome

    def find(self, p_key, update_cache=True):
        try:
            p = self.players[p_key]
        except KeyError:
            return None
        if update_cache:
            self.mark_recent_player(p_key)
        return self.convert_to_player(p)

    def get_player_name(self, p_key):
        try:
            p = self.players[p_key]
        except KeyError:
            return None
        return p.get_name()

    def convert_to_player(self, player):
        if type(player) == type(0):
            try:
                player = self.players[player]
            except KeyError:
                return None

        if player.__class__ is aig_m.AIGenome:
            player = self.factory.create_player(player)
        else:
            # HumanPlayers are stored directly
            pass
        return player

    def get_max_id(self):
        return misc().setdefault("max_id", 0)

    def next_id(self):
        curr_id = self.get_max_id() + 1
        misc()["max_id"] = curr_id
        z_m.sync()
        return curr_id

