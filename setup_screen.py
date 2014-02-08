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

    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        self.ids.black_type_id.bind(val=self.populate_black_players)
        self.ids.white_type_id.bind(val=self.populate_white_players)

    def populate_black_players(self, *args):
        ptw = self.ids.black_type_id
        self.populate_players(ptw, BLACK)

    def populate_white_players(self, *args):
        ptw = self.ids.white_type_id
        self.populate_players(ptw, WHITE)

    def populate_players(self, ptw, colour):
        if ptw.val == 'Computer':
            self.player_names[colour] = ["DT", "Killer"]
        else:
            self.player_names[colour] = ["Fredo", "BC"]

    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        if g:
            self.app.start_game(g, self.size)

    def create_game(self):
        self.game = self.app.games_mgr.create_game()
        self.ids.start_button.text = "Start Game"

    def alter_game(self, game):
        self.game = game
        self.set_GUI_from_game(self.game)
        self.ids.start_button.text = "Resume Game"

    def set_up_game_from_GUI(self):
        try:
            bs = int(self.ids.bs_id.text)
        except ValueError:
            self.app.display_error("Select a board size")
            return
        
        rstr = self.ids.rules_id.text
        try:
            r = rules.Rules(bs, rstr)
        except UnknownRuleType, e:
            self.app.display_error("Select the rules type")
            return

        # TODO: pass in player type
        player1 = self.pm.find_by_name(self.ids.bpl_id.text)
        player2 = self.pm.find_by_name(self.ids.wpl_id.text)

        self.game.setup(r, player1, player2)
        return self.game

    def set_GUI_from_game(self, g):
        self.ids.bpl_id.text = g.get_player_name(BLACK)
        self.ids.wpl_id.text = g.get_player_name(WHITE)
        self.ids.bs_id.text = str(g.rules.size)
        self.ids.rules_id.text = g.rules.get_type_name()
        # TODO: Player type, AI Parameters?

