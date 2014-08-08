from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher

import checkbox_list as cb_l

from pentai.gui.player_screen import *
import pentai.ai.ai_genome as aig_m

# TODO: Make a reusable class for this.
class GenomeProperties(EventDispatcher):
    inst = aig_m.AIGenome("Whatever")

    def genome2screen(self, g=None):
        """ Copy from genome g into self's namespace """
        if g is None:
            # Copy from the default genome instance
            g = self.inst

        for k,v in g.__dict__.iteritems():
            setattr(self, k, v)

    def screen2genome(self, unused=None):
        """ Copy from our namespace into the default global instance """
        for k,v in self.inst.__dict__.iteritems():
            setattr(self.inst, k, getattr(self, k))
        return self.inst

# TODO: Move this into the class somehow
for attr_name, val in GenomeProperties.inst.__dict__.iteritems():
    setattr(GenomeProperties, attr_name, Property(val, allownone=True))

class AIPlayerScreen(PlayerScreen):
    genome = GenomeProperties()

    player_class = aig_m.AIGenome
    player_type_str = "AI"

    def edit_player(self, name):
        g = self.pm.find_genome_by_name(name)
        self.genome.genome2screen(g)
        self.genome.screen2genome()

    def update_player(self, player, new_name):
        self.genome.screen2genome()
        self.genome.inst.p_name = new_name
        player.genome.__dict__.update(self.genome.inst.__dict__)

    def get_players(self):
        return self.pm.get_ai_player_names()

    def cancel(self, unused=None):
        self.genome.genome2screen()

    def show_help(self):
        self.app.show_ai_help()
