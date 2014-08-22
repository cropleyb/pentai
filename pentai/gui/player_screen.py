from kivy.properties import *
from kivy.uix.screenmanager import Screen

from pentai.base.defines import *

class PlayerScreen(Screen):
    create_text = "Create One"
    player_names = ListProperty([])
    rename_req = "Give me a Name"
    rename_text = StringProperty(rename_req)

    def __init__(self, *args, **kwargs):
        super(PlayerScreen, self).__init__(*args, **kwargs)

        self.ids.player_spinner_id.bind(text=self.select_player)
        self.ids.player_spinner_id.text = self.create_text

        self.ids.name_id.bind(focus=self.on_rename_focus)
        self.ids.name_id.bind(on_text_validate=self.save_with_check)

    def set_player_names(self, names):
        self.player_names = names

    def on_rename_focus(self, instance, value):
        if value:
            # Focus
            if self.rename_text == self.rename_req:
                # Create player -> empty the field
                self.rename_text = ""

    def select_player(self, spinner, val):
        # TODO: Trigger save somehow?

        if val == self.create_text:
            self.rename_text = self.rename_req
            return
        if val != "":
            self.rename_text = val
        self.edit_player(val)

    def edit_player(self, name):
        if name != self.rename_req:
            g = self.pm.find_by_name(name)

    def on_enter(self):
        self.refresh_names()
        if self.ids.player_spinner_id.text == self.create_text:
            self.ids.name_id.text = self.rename_req
            self.ids.name_id.focus = False

    def on_leave(self):
        self.save()

    def refresh_names(self):
        pns = [self.create_text]
        pns.extend(sorted(self.get_players()))
        self.set_player_names(pns)

    def menu(self, unused=None):
        self.app.return_screen()

    def cancel(self, unused=None):
        if self.ids.name_id.text != self.rename_req:
            self.ids.name_id.text = self.rename_text

    def delete(self, unused=None):
        pl = self.pm.find_by_name(self.ids.name_id.text, self.player_type_str)
        if pl:
            self.ids.name_id.text = self.rename_req
            self.pm.remove(pl.p_key)
            self.rename_text = self.rename_req
            self.ids.name_id.focus = False
            self.refresh_names()
            self.set_spinner_val(self.create_text)

    def save_with_check(self, unused=None):
        if self.ids.name_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set.
            self.app.display_error("Please choose a name before saving")
            return
        self.save()

    def save(self, unused=None):
        if self.ids.name_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set, ignore
            return

        # The entered name
        pn = self.ids.name_id.text
        if not pn:
            return

        if pn != self.create_text and pn and self.rename_text:
            # Rename
            pl = self.pm.find_genome_by_name(self.rename_text, self.player_type_str)
            if not pl:
                return
            pl.p_name = pn
            create = False
        else:
            if (pn == self.rename_req) or (not pn):
                return
            # Create
            pl = self.player_class(pn)
            create = True

        if pl:
            self.update_player(pl, pn, create)
            self.pm.save(pl)
            self.set_spinner_val(pn)
            self.refresh_names()

            defaults = self.app.get_game_defaults()
            defaults.set_player_of_type(pl.get_type(), pl.p_key)

    def update_player(self, player, new_name, create):
        pass

    def set_spinner_val(self, new_val):
        self.ids.player_spinner_id.text = new_val

    def show_help(self):
        self.app.show_human_help()

