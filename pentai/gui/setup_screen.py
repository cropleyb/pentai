from kivy.properties import *
from pentai.gui.screen import Screen

import pentai.base.rules as r_m
from pentai.base.defines import *
from pentai.base.pente_exceptions import *
import pentai.base.logger as log

from pentai.gui.game_defaults import *
import pentai.gui.checkbox_list as cb_l

import pentai.db.misc_db as m_m

def misc():
    return m_m.get_instance()

from kivy.uix.spinner import *

screen = None

class HighlightableOption(SpinnerOption):

    def on_text(self, widget, text):
        screen.text_to_widget["%s_id" % text] = widget

class SetupScreen(Screen):
    player_names = ListProperty([[], [], []])
    time_control = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        global screen
        screen = self

        self.game = None
        self.repop = False
        self.initialised = False
        
        self.text_to_widget = {}
        self.ids.wpl_id.option_cls = HighlightableOption

        # Updating a player name triggers set_player_name
        func = lambda v,dt: self.set_player_name(P1, v.text)
        self.ids.bpl_id.bind(text=func)
        func = lambda v,dt: self.set_player_name(P2, v.text)
        self.ids.wpl_id.bind(text=func)

        # Updating the player type triggers set_player_type
        func = lambda v,dt: self.set_player_type(P1, v.val)
        self.ids.black_type_id.bind(val=func)
        func = lambda v,dt: self.set_player_type(P2, v.val)
        self.ids.white_type_id.bind(val=func)

        # Update the rules explanation text
        func = lambda v,dt: self.show_rules_explanation()
        self.ids.rules_id.bind(text=func)

        # Opening player list triggers updated_players
        self.ids.wpl_id.bind(is_open=self.on_p2_open)

        self.defaults = None
        # TODO: Timer default

    def on_p2_open(self, spinner, is_open):
        self.updated_players()

    def on_pre_enter(self):
        if not self.initialised:
            self.initialised = True

        self.show_rules_explanation()
        self.set_GUI_from_defaults(self.get_defaults())
        self.populate_all_players()

    def on_enter(self):
        self.updated_players()

    def set_player_name(self, colour, player_name):
        if not self.repop:
            p_key = self.pm.get_p_key_from_name(player_name)
            self.get_defaults().set_player(colour, p_key)
            self.populate_all_players()

    def set_player_type(self, colour, player_type):
        if self.initialised:
            if player_type == "Computer":
                player_type = "AI"
            self.get_defaults().set_type(colour, player_type)
            self.populate_all_players()

    def get_default_player_name(self, colour):
        p_key = self.get_defaults().get_player(colour)
        if not p_key:
            return ""
        p_name = self.pm.get_player_name(p_key)
        return p_name

    def populate_all_players(self):
        self.repop = True
        self.ids.bpl_id.text = self.get_default_player_name(P1)
        self.ids.wpl_id.text = self.get_default_player_name(P2)
        self.repop = False

        self.populate_black_player_list()
        self.populate_white_player_list()

    def populate_black_player_list(self, *args):
        ptb = self.get_defaults().get_type(P1)
        self.populate_player_list(ptb, P1)

    def populate_white_player_list(self, *args):
        ptw = self.get_defaults().get_type(P2)
        self.populate_player_list(ptw, P2)
        try:
            # Callback to guide
            self.updated_players()
        except AttributeError:
            pass

    def populate_player_list(self, pt, colour):
        rpl = self.pm.get_recent_player_names(pt, 30)
        self.player_names[colour] = sorted(rpl)

    def show_rules_explanation(self):
        text = self.ids.rules_id.text
        re_id = self.ids.rules_explanation_id
        if text == "Standard":
            re_id.text = "Games can be won by capturing 5 pairs, or by getting 5 in a row."
        elif text == "Tournament":
            re_id.text = "Same as Standard rules, but the 2[sup]nd[/sup] move by the 1[sup]st[/sup] player cannot be close to the centre."
        elif text == "5-In-A-Row":
            re_id.text = "Games can ONLY be won by getting 5 in a row. The first move can be anywhere."
        else:
            assert(text == "Unknown Rules type")

    def time_control_text(self, tc):
        if tc == 0:
            return "No Limit"
        mins = tc / 1
        secs = int((tc % 1) * 60)
        return '%d:%02d' % (mins, secs)

    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        if g:
            self.app.start_game(g)

    def create_game(self):
        self.game = self.app.games_mgr.create_game()
        self.ids.title_id.text = "New Game"
        self.ids.start_game_id.text = "Start Game"

    def alter_game(self, game):
        self.game = game
        self.set_defaults_from_game(game)
        self.ids.title_id.text = "Edit Game"
        self.ids.start_game_id.text = "Resume Game"

    def get_defaults(self):
        if self.defaults == None:
            self.defaults = self.app.get_game_defaults()
        return self.defaults

    def set_defaults_from_game(self, game):
        self.get_defaults().add_game(game)

    def set_up_game_from_GUI(self):
        try:
            bs = int(self.ids.bs_id.text)
        except ValueError:
            self.app.display_message("Select a board size")
            return
        
        rstr = self.ids.rules_id.text
        time_control = self.time_control
        try:
            r = r_m.Rules(bs, rstr, time_control)
        except UnknownRuleType, e:
            self.app.display_message("Select the rules type")
            return

        # TODO: pass in player type
        # TODO: Copy & paste
        p1_t = self.ids.black_type_id.val
        if p1_t == "Computer":
            p1_t = "AI"
        p1 = self.pm.find_by_name(self.ids.bpl_id.text, p1_t)
        if not p1:
            self.app.display_message("Select a player for Black")
            return

        p2_t = self.ids.white_type_id.val
        if p2_t == "Computer":
            p2_t = "AI"
        p2 = self.pm.find_by_name(self.ids.wpl_id.text, p2_t)
        if not p2:
            self.app.display_message("Select a player for White")
            return

        self.game.setup(r, p1, p2)
        self.set_defaults_from_game(self.game)
        return self.game
    
    def set_GUI_from_defaults(self, g): # TODO: don't pass g in?
        self.ids.bpl_id.text = self.get_default_player_name(P1)
        self.ids.wpl_id.text = self.get_default_player_name(P2)
        bpt = g.get_player_type(P1)
        wpt = g.get_player_type(P2)
        self.ids.black_type_id.set_active(bpt)
        self.ids.white_type_id.set_active(wpt)
        self.ids.bs_id.text = str(g.get_size())
        self.ids.rules_id.text = g.get_rules_type_name()
        self.time_control = g.get_total_time()
        self.ids.time_control_id.value = self.time_control

