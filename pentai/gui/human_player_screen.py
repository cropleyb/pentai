from kivy.properties import *
from kivy.uix.screenmanager import Screen

from scrollable_label import *

from pentai.base.human_player import *

import checkbox_list as cb_l
from popup import *



class HumanPlayerScreen(Screen):
    create_text = "Create one"
    current_name = StringProperty(create_text)
    player_names = ListProperty([])
    rename_req = "Give me a name"
    rename_text = StringProperty(rename_req)

    def __init__(self, *args, **kwargs):
        super(HumanPlayerScreen, self).__init__(*args, **kwargs)

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
        g = self.pm.find_by_name(name)
        # TODO?
        '''
        if g is None:
            g = self.pm.find_genome_by_name(name)
        self.genome.genome2screen(g)
        self.genome.screen2genome()
        '''

    def on_enter(self):
        self.refresh_names()

    def refresh_names(self):
        self.player_names = [self.create_text]
        pns = self.pm.get_human_player_names()
        self.player_names.extend(sorted(pns))

    def menu(self, unused=None):
        self.app.return_screen()

    def cancel(self, unused=None):
        if self.ids.rename_id.text != self.rename_req:
            self.ids.rename_id.text = self.rename_text

    def save(self, unused=None):
        if self.ids.rename_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set.
            self.app.display_error("Please choose a name first")
            return
        '''
        self.genome.p_name = self.ids.rename_id.text
        self.genome.screen2genome()
        self.pm.save(self.genome.inst.clone())
        '''
        hpn = self.ids.rename_id.text
        hp = HumanPlayer(hpn)
        self.pm.save(hp)
        self.current_name = hpn
        self.refresh_names()

    def show_help(self):
        help_text = """You can either edit an existing player by selecting their name, or create a new one (leave the top box with "Create One", and type in the name immediately below.
There are several settings that can be adjusted for a given AI player profile:
    Depth: Controls how many moves the AI looks ahead each move.
    Vision: How often does the AI miss a move possibility entirely?
    Openings book: Should the AI be able to refer to previous games?
    Lines/Captures: How much value should the AI place on lines versus captures?
    Judgement: How well should the AI judge the value of positions?

Several profiles are included, have a look at and experiment with their configurations, or create your own.

"""
        st = ScrollableLabel(text=help_text)
        MessagePopup(title='Help', content=st).open()
		
