from kivy.properties import *
from pentai.gui.screen import Screen
from kivy.uix.spinner import *
from kivy.clock import Clock

from pentai.base.defines import *

# TODO: Put this in its own file?
class HighlightableOption(SpinnerOption):
    def __init__(self, *args, **kwargs):
        super(HighlightableOption, self).__init__(*args, **kwargs)
        self.bind(on_press=lambda option: self.on_preselect(option.text))

    def on_text(self, widget, text):
        self.screen.text_to_widget["%s_id" % text] = widget

    def on_preselect(self, new_text):
        self.screen.preselect(new_text)

class PlayerScreen(Screen):
    create_text = "Create"
    select_text = "Select"
    player_names = ListProperty([])
    #rename_req = "Give me a Name"
    rename_req = "Create"
    rename_text = StringProperty(rename_req)

    def __init__(self, *args, **kwargs):
        super(PlayerScreen, self).__init__(*args, **kwargs)

        self.text_to_widget = {}

        spinner = self.ids.player_spinner_id
        spinner.bind(text=self.select_player)
        spinner.text = self.select_text

        self.ids.name_id.bind(focus=self.on_rename_focus)
        self.ids.name_id.bind(on_text_validate=self.save_with_check)

        class HiOp(HighlightableOption):
            screen = self
        spinner = self.ids.player_spinner_id
        spinner.option_cls = HiOp
        Clock.schedule_once(self.bind_players, 0.1)

    def preselect(self, new_text):
        self.save()

    def bind_players(self, *args):
        # Opening player list triggers updated_players
        self.refresh_names()
        self.ids.player_spinner_id.bind(is_open=self.on_p_open)

    def on_p_open(self, spinner, is_open):
        if is_open:
            # This is to update the Guide
            self.updated_players()

    def set_player_names(self, names):
        self.player_names = names

    def on_rename_focus(self, instance, value):
        if value:
            # Focus
            if self.rename_text == self.rename_req:
                # Create player -> empty the field
                self.rename_text = ""
            self.app.guide.on_focus(instance)

    def select_player(self, spinner, val):
        if val == self.create_text:
            spinner = self.ids.player_spinner_id
            spinner.text = self.select_text
            return
        if val == self.select_text:
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

    def show_menu_screen(self):
        self.save()
        self.app.show_menu_screen()

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
        self.set_spinner_val(self.select_text)

    def save_with_check(self, unused=None):
        if self.ids.name_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set.
            self.app.display_message("Please choose a name")
            return
        self.save()
        self.app.guide.on_enter("Human")

    def save(self, unused=None):
        if self.ids.name_id.text in [self.rename_req, ""]:
            # Attempt to save with no name set, ignore
            return

        # The entered name
        pn = self.ids.name_id.text
        if not pn:
            return

        if (not pn in (self.create_text, self.select_text)) \
                and pn and self.rename_text:
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

