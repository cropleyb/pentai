'''
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


import rules
import game
import human_player
import ai_player
'''
from kivy.uix.screenmanager import Screen
from kivy.properties import *

'''
Start/settings screen
Player selection, with default of last selected.
Load game button - go to load screen

Options screen:
Help
Mark recent moves
Mark recent captures
Confirm moves
Sound effects volume
Music volume
Start/Resume

Help Screen:
Rules
Controls
'''

class OptionsScreen(Screen):
    mark_moves = BooleanProperty(True)
    mark_captures = BooleanProperty(True)
    confirm_moves = BooleanProperty(False)
    sound_effects_vol = NumericProperty(0)
    music_vol = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(OptionsScreen, self).__init__(*args, **kwargs)

