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

import pdb

def create_player(player_type_widget, player_name, max_depth):
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
        
    def load_file(self, filename):
        if filename:
            self.set_GUI_from_file(filename)
        else:
            self.ids.start_button.text = "Start Game"

    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        self.app.start_game(g, self.size)

    def set_up_game_from_GUI(self):
        bs = int(self.ids.bs_id.val)
        rstr = self.ids.rules_id.val
        r = rules.Rules(bs, rstr)

        max_depth = int(self.ids.max_depth_id.val)
        player1 = create_player(self.ids.black_type_id, self.ids.black_name_id.text, max_depth)
        player2 = create_player(self.ids.white_type_id, self.ids.white_name_id.text, max_depth)

        g = self.app.games_mgr.create_game(r, player1, player2)
        return g

    def set_GUI_from_file(self, filename):
        f = open(filename)
        # TODO: New method set GUI from game.
        #g = self.app.games_mgr.create_game(r, player1, player2)
        g = game.Game(None, None, None) # Hmmm. TODO
        g.configure_from_str(f.read())
        self.ids.start_button.text = "Resume"
        self.ids.black_name_id.text = g.get_player_name(BLACK)
        self.ids.white_name_id.text = g.get_player_name(WHITE)
        self.ids.bs_id.set_active(g.rules.size)
        self.ids.rules_id.set_active(g.rules.type_str)
