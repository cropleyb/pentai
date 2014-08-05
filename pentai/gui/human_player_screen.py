from kivy.properties import *

from pentai.base.defines import *
from pentai.base.human_player import *
from pentai.gui.player_screen import *

class HumanPlayerScreen(PlayerScreen):
    player_class = HumanPlayer
    player_type_str = "Human"

