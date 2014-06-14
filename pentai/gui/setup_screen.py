from kivy.properties import *
from kivy.uix.screenmanager import Screen

import pentai.base.rules as r_m
from pentai.base.defines import *
from pentai.base.pente_exceptions import *

import pentai.db.misc_db as m_m
from pentai.gui.game_defaults import *

def misc():
    return m_m.get_instance()

class SetupScreen(Screen):
    player_names = ListProperty([[], [], []])
    time_control = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        self.game = None
        self.repop = False
        self.defaults = misc().setdefault("game_defaults", GameDefaults())

        # Updating a player name triggers set_player_name
        func = lambda v,dt: self.set_player_name(BLACK, v.text)
        self.ids.bpl_id.bind(text=func)
        func = lambda v,dt: self.set_player_name(WHITE, v.text)
        self.ids.wpl_id.bind(text=func)

        # Updating the player type triggers set_player_type
        func = lambda v,dt: self.set_player_type(BLACK, v.val)
        self.ids.black_type_id.bind(val=func)
        func = lambda v,dt: self.set_player_type(WHITE, v.val)
        self.ids.white_type_id.bind(val=func)

    def on_pre_enter(self):
        self.set_GUI_from_game(self.defaults)
        self.populate_all_players()

    def set_player_name(self, colour, player_name):
        if not self.repop:
            self.defaults.set_name(colour, player_name)
            self.populate_all_players()

    def set_player_type(self, colour, player_type):
        if player_type == "Computer":
            player_type = "AI"
        self.defaults.set_type(colour, player_type)
        self.populate_all_players()

    def populate_all_players(self):
        self.repop = True
        self.ids.bpl_id.text = self.defaults.get_player_name(BLACK)
        self.ids.wpl_id.text = self.defaults.get_player_name(WHITE)
        self.repop = False

        self.populate_black_player_list()
        self.populate_white_player_list()

    def populate_black_player_list(self, *args):
        ptb = self.defaults.get_type(BLACK)
        self.populate_player_list(ptb, BLACK)

    def populate_white_player_list(self, *args):
        ptw = self.defaults.get_type(WHITE)
        self.populate_player_list(ptw, WHITE)

    def populate_player_list(self, pt, colour):
        rpl = self.pm.get_recent_player_names(pt, 30)
        self.player_names[colour] = sorted(rpl)

    def time_control_text(self, tc):
        if tc == 0:
            return "No Limit"
        mins = tc / 1
        secs = int((tc % 1) * 60)
        return '%d:%02d' % (mins, secs)

    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        if g:
            self.app.start_game(g, self.size)

    def create_game(self):
        self.game = self.app.games_mgr.create_game()
        self.ids.start_game_id.text = "Start Game"

    def alter_game(self, game):
        self.game = game
        self.set_GUI_from_game(self.game)
        self.ids.start_game_id.text = "Resume Game"

    def set_up_game_from_GUI(self):
        try:
            bs = int(self.ids.bs_id.text)
        except ValueError:
            self.app.display_error("Select a board size")
            return
        
        rstr = self.ids.rules_id.text
        time_control = self.time_control
        try:
            r = r_m.Rules(bs, rstr, time_control)
        except UnknownRuleType, e:
            self.app.display_error("Select the rules type")
            return

        # TODO: pass in player type
        # TODO: Copy & paste
        p1_t = self.ids.black_type_id.val
        if p1_t == "Computer":
            p1_t = "AI"
        p1 = self.pm.find_by_name(self.ids.bpl_id.text, p1_t)
        if not p1:
            self.app.display_error("Select a player for Black")
            return

        p2_t = self.ids.white_type_id.val
        if p2_t == "Computer":
            p2_t = "AI"
        p2 = self.pm.find_by_name(self.ids.wpl_id.text, p2_t)
        if not p2:
            self.app.display_error("Select a player for White")
            return

        self.game.setup(r, p1, p2)
        self.defaults.play_game((p1_t,p1.get_name()), (p2_t, p2.get_name()), self.game.get_rules())
        return self.game
    
    def set_GUI_from_game(self, g):
        self.ids.bpl_id.text = g.get_player_name(BLACK)
        self.ids.wpl_id.text = g.get_player_name(WHITE)
        self.ids.bs_id.text = str(g.get_size())
        self.ids.rules_id.text = g.get_rules_type()
        # TODO: Player type, AI Parameters?

