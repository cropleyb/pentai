from kivy.properties import *
from kivy.uix.screenmanager import Screen

from scrollable_label import *
from pentai.base.defines import *

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

        self.ids.name_id.bind(focus=self.on_rename_focus)
        self.ids.name_id.bind(on_text_validate=self.save)

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

    def on_enter(self):
        self.refresh_names()

    def on_leave(self):
        self.save()

    def refresh_names(self):
        self.player_names = [self.create_text]
        pns = self.pm.get_human_player_names()
        self.player_names.extend(sorted(pns))

    def menu(self, unused=None):
        self.app.return_screen()

    def cancel(self, unused=None):
        if self.ids.name_id.text != self.rename_req:
            self.ids.name_id.text = self.rename_text

    def delete(self, unused=None):
        #st()
        if self.ids.name_id.text != self.rename_req:
            hp = self.pm.find_by_name(self.ids.name_id.text, "Human")
            self.ids.name_id.text = self.rename_req
            self.pm.remove(hp.p_key)
            self.rename_text = self.rename_req
            self.refresh_names()
            #st()
            self.set_spinner_val(self.create_text)

    def save(self, unused=None):
        if self.ids.name_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set.
            self.app.display_error("Please choose a name first")
            return

        # The entered name
        hpn = self.ids.name_id.text
        if self.current_name != self.create_text:
            # Rename
            hp = self.pm.find_by_name(self.rename_text, "Human")
            self.pm.remove(hp.p_key)
            hp.p_name = hpn
        else:
            # Create
            hp = HumanPlayer(hpn)

        self.pm.save(hp)
        self.set_spinner_val(hpn)
        self.refresh_names()

    def set_spinner_val(self, new_val):
        self.current_name = new_val
        self.ids.player_spinner_id.text = new_val

    def show_help(self):
        self.app.show_human_help()

