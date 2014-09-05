from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
from kivy.clock import Clock

import checkbox_list as cb_l

from pentai.gui.player_screen import *
import pentai.ai.ai_genome as aig_m

from kivy.uix.spinner import *

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

screen = None

# TODO: Put this in its own file
class HighlightableOption(SpinnerOption):
    def on_text(self, widget, text):
        screen.text_to_widget["%s_id" % text] = widget

class AIPlayerScreen(PlayerScreen):
    genome = GenomeProperties()

    player_class = aig_m.AIGenome
    player_type_str = "AI"

    def __init__(self, *args, **kwargs):
        super(AIPlayerScreen, self).__init__(*args, **kwargs)

        global screen
        screen = self

        self.text_to_widget = {}
        self.ids.player_spinner_id.option_cls = HighlightableOption
        Clock.schedule_once(self.bind_players, 0.1)

    def bind_players(self, *args):
        # Opening player list triggers updated_players
        self.refresh_names()
        self.ids.player_spinner_id.bind(is_open=self.on_p_open)

    def on_p_open(self, spinner, is_open):
        if is_open:
            self.updated_players()

    def edit_player(self, name):
        g = self.pm.find_genome_by_name(name)
        self.genome.genome2screen(g)
        self.genome.screen2genome()

    def update_player(self, player, new_name, create):
        self.genome.screen2genome()
        self.genome.inst.p_name = new_name
        player.__dict__.update(self.genome.inst.__dict__)
        if create:
            player.p_key = None
            if hasattr(player, "_saved_name"):
                # TODO: This is a bit ugly, it would be nice to contain
                # this to the PlayersMgr
                player._saved_name = None

    def get_players(self):
        return self.pm.get_ai_player_names()

    def cancel(self, unused=None):
        self.genome.genome2screen()

    def show_help(self):
        self.app.show_ai_help()
