from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import *
from kivy.uix.screenmanager import Screen

import rules
import game
import human_player
import ai_genome
import ai_factory

import checkbox_list as cb_l

from defines import *

def create_player(player_type_widget, player_name, max_depth):
    # TODO: find_or_create_player
    if player_type_widget.val == 'Computer':
        # TODO: This doesn't really belong here.
        genome = ai_genome.AIGenome(player_name)
        genome.max_depth = max_depth
        # TODO: configure openings book usage

        aif = ai_factory.AIFactory()
        p = aif.create_player(genome)
    else:
        p = human_player.HumanPlayer(player_name)
    return p

class SetupScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)
    
    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        self.app.start_game(g, self.size)

    def create_game(self):
        self.game = self.app.games_mgr.create_game()
        self.ids.start_button.text = "Start Game"

    def alter_game(self, game):
        self.game = game
        self.set_GUI_from_game(self.game)
        self.ids.start_button.text = "Resume Game"

    def set_up_game_from_GUI(self): # TODO: Rename to set_game_from_GUI
        bs = int(self.ids.bs_id.val)
        rstr = self.ids.rules_id.val
        r = rules.Rules(bs, rstr)

        max_depth = int(self.ids.max_depth_id.val)

        # TODO: Reuse existing players?!
        player1 = create_player(self.ids.black_type_id, self.ids.black_name_id.text, max_depth)
        player2 = create_player(self.ids.white_type_id, self.ids.white_name_id.text, max_depth)

        self.game.setup(r, player1, player2)
        return self.game

    def set_GUI_from_game(self, g):
        self.ids.black_name_id.text = g.get_player_name(BLACK)
        self.ids.white_name_id.text = g.get_player_name(WHITE)
        self.ids.bs_id.set_active(g.rules.size)
        self.ids.rules_id.set_active(g.rules.get_type_name())
        # TODO: Player type, AI Parameters?

