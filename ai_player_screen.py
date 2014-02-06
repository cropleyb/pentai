
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import *
from kivy.uix.screenmanager import Screen

import rules
import game
import human_player
import ai_genome
import ai_factory

import checkbox_list as cb_l

from kivy.event import EventDispatcher

from defines import *

# TODO: Make a reusable class for this.
class GenomeProperties(EventDispatcher):
    inst = ai_genome.AIGenome("Whatever")

    def genome2screen(self, g=None):
        ''' Copy from genome g into self's namespace '''
        if g is None:
            # Copy from the default genome instance
            g = self.inst

        for k,v in g.__dict__.iteritems():
            setattr(self, k, v)

    def screen2genome(self, unused=None):
        ''' Copy from our namespace into the default global instance '''
        for k,v in self.inst.__dict__.iteritems():
            setattr(self.inst, k, getattr(self, k))
        return self.inst

# TODO: Move this into the class somehow
for attr_name, val in GenomeProperties.inst.__dict__.iteritems():
    setattr(GenomeProperties, attr_name, Property(val, allownone=True))

class AIPlayerScreen(Screen):
    current_name = StringProperty("Choose one")
    player_names = ListProperty([])
    genome = GenomeProperties()

    def __init__(self, *args, **kwargs):
        super(AIPlayerScreen, self).__init__(*args, **kwargs)

        self.ids.player_spinner_id.bind(text=self.select_player)

    # TODO: Does this work?
    def on_genome(self, *args):
        pass
        #print "Genome was updated %s, %s" % args

    def select_player(self, spinner, val):
        if val == "Create player":
            return
        self.edit_player(val)

    def edit_player(self, name):
        g = self.pm.find_genome_by_name(name)
        if g is None:
            st()
            g = self.pm.find_genome_by_name(name)
        self.genome.genome2screen(g)
        self.genome.screen2genome()

    def on_enter(self):
        self.player_names = sorted(self.pm.get_player_names())

    def menu(self, unused=None):
        self.app.return_screen()

    def cancel(self, unused=None):
        self.genome.genome2screen()

    def save(self, unused=None):
        self.genome.screen2genome()
        self.pm.save(self.genome.inst.clone())

    def create_player(self):
        # TODO
        pass


