
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

from defines import *


class AIPlayerScreen(Screen):
    current_name = StringProperty("Choose one")
    player_names = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(AIPlayerScreen, self).__init__(*args, **kwargs)

        self.ids.player_spinner_id.bind(text=self.selected_player)

    '''
    def on_genome(self, *args):
        print "Genome was updated %s, %s" % args
    '''

    def selected_player(self, spinner, val):
        if val == "Create player":
            return
        self.edit_player(val)

    def on_enter(self):
        self.player_names = sorted(self.pm.get_player_names())

    def save(self, unused=None):
        for k,v in working_genome.__dict__.iteritems():
            setattr(working_genome, k, getattr(self, k))
        st()
        #self.pm.save(working_genome)
        self.app.return_screen()

    def cancel(self, unused=None):
        self.app.return_screen()

    def create_player(self):
        # TODO
        pass

    def edit_player(self, name):
        g = self.pm.find_genome_by_name(name)

        for k,v in g.__dict__.iteritems():
            setattr(self, k, v)


# Set up many properties at once.
# TODO: Make a reusable class for this.
working_genome = ai_genome.AIGenome("Whatever")

for attr_name, val in working_genome.__dict__.iteritems():
    setattr(AIPlayerScreen, attr_name, Property(val))
