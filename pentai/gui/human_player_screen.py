from kivy.properties import *

from pentai.base.defines import *
from pentai.base.human_player import *
from pentai.gui.player_screen import *

class HumanPlayerScreen(PlayerScreen):
    player_class = HumanPlayer
    player_type_str = "Human"

    def get_players(self):
        return self.pm.get_human_player_names()
