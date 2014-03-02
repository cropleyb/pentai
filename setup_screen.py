from kivy.properties import *
from kivy.uix.screenmanager import Screen

import rules
import game
import human_player
import ai_genome
import ai_factory

from defines import *
from pente_exceptions import *

class SetupScreen(Screen):
    player_names = ListProperty([[], [], []])
    time_control = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        self.ids.black_type_id.bind(val=self.populate_black_players)
        self.ids.white_type_id.bind(val=self.populate_white_players)

    def on_enter(self):
        self.populate_black_players()
        self.populate_white_players()

    def populate_black_players(self, *args):
        ptb = self.ids.black_type_id
        white_player = self.ids.wpl_id.text
        self.populate_players(ptb.val, BLACK, exclude=white_player)
        self.ids.bpl_id.text = self.player_names[BLACK][0]

    def populate_white_players(self, *args):
        ptw = self.ids.white_type_id
        black_player = self.ids.bpl_id.text
        self.populate_players(ptw.val, WHITE, exclude=black_player)
        self.ids.wpl_id.text = self.player_names[WHITE][0]

    def populate_players(self, pt, colour, exclude):
        rpl = self.pm.get_recent_player_names(pt, 30)
        try:
            rpl.remove(exclude)
        except:
            pass
        self.player_names[colour] = rpl

    def time_control_text(self, tc):
        if tc == 0:
            return "No Limit"
        return '{}'.format(int(tc))

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
            r = rules.Rules(bs, rstr, time_control)
        except UnknownRuleType, e:
            self.app.display_error("Select the rules type")
            return

        # TODO: pass in player type
        p1_t = self.ids.black_type_id.val
        player1 = self.pm.find_by_name(self.ids.bpl_id.text, p1_t)
        if not player1:
            self.app.display_error("Select a player for Black")
            return

        p2_t = self.ids.white_type_id.val
        player2 = self.pm.find_by_name(self.ids.wpl_id.text, p2_t)
        if not player2:
            self.app.display_error("Select a player for White")
            return

        self.game.setup(r, player1, player2)
        return self.game

    def set_GUI_from_game(self, g):
        self.ids.bpl_id.text = g.get_player_name(BLACK)
        self.ids.wpl_id.text = g.get_player_name(WHITE)
        self.ids.bs_id.text = str(g.rules.size)
        self.ids.rules_id.text = g.rules.get_type_name()
        # TODO: Player type, AI Parameters?

