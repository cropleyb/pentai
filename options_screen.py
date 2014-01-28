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


import mock

def s2b(state):
    """ state string to boolean """
    return state == "down"

class OptionsScreen(Screen):
    # TODO
    sound_effects_vol = NumericProperty(0)
    music_vol = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(OptionsScreen, self).__init__(*args, **kwargs)

    def get_pente_screen(self):
        if self.app.pente_screen:
            return self.app.pente_screen
        return mock.Mock() # Hacky Null object pattern

    def set_mark_moves(self, state):
        self.get_pente_screen().set_mark_moves(s2b(state))

    def set_mark_captures(self, state):
        self.get_pente_screen().set_mark_captures(s2b(state))

    def set_confirm_mode(self, state):
        if state == "None":
            state = None
        self.get_pente_screen().set_confirm_mode(state)

