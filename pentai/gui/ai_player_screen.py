from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher

import checkbox_list as cb_l

import pentai.ai.ai_genome as aig_m



# TODO: Make a reusable class for this.
class GenomeProperties(EventDispatcher):
    inst = aig_m.AIGenome("Whatever")

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
    create_text = "Create one"
    current_name = StringProperty(create_text)
    player_names = ListProperty([])
    genome = GenomeProperties()
    rename_req = "Give me a name"
    rename_text = StringProperty(rename_req)

    def __init__(self, *args, **kwargs):
        super(AIPlayerScreen, self).__init__(*args, **kwargs)

        self.ids.player_spinner_id.bind(text=self.select_player)
        self.current_name = self.create_text

        self.ids.rename_id.bind(focus=self.on_rename_focus)

    def on_rename_focus(self, instance, value):
        if value:
            # Focus
            if self.rename_text == self.rename_req:
                # Create player -> empty the field
                self.rename_text = ""

    def select_player(self, spinner, val):
        if val == self.create_text:
            self.rename_text = self.rename_req
            return
        if val != "":
            self.rename_text = val
        self.edit_player(val)

    def edit_player(self, name):
        g = self.pm.find_genome_by_name(name)
        if g is None:
            g = self.pm.find_genome_by_name(name)
        self.genome.genome2screen(g)
        self.genome.screen2genome()

    def on_enter(self):
        self.refresh_names()

    def refresh_names(self):
        self.player_names = [self.create_text]
        pns = self.pm.get_ai_player_names()
        self.player_names.extend(sorted(pns))

    def menu(self, unused=None):
        self.app.return_screen()

    def cancel(self, unused=None):
        self.genome.genome2screen()

    def save(self, unused=None):
        if self.ids.rename_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set.
            self.app.display_error("Please choose a name first")
            return
        self.genome.p_name = self.ids.rename_id.text
        self.genome.screen2genome()
        self.pm.save(self.genome.inst.clone())
        self.current_name = self.genome.p_name
        self.refresh_names()

    def show_help(self):
        self.app.show_ai_help()
