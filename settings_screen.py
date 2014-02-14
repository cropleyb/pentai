from kivy.uix.screenmanager import Screen
from kivy.properties import *

from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from defines import *

'''
Start/settings screen
Player selection, with default of last selected.
Load game button - go to load screen

Settings screen:
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

class SettingsScreen(Screen):
    # TODO
    sound_effects_vol = NumericProperty(0)
    music_vol = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)

    def build(self):
        gl = GridLayout(cols=1)
        self.add_widget(gl)

        gl.add_widget(self.settings)

        bw = Button(text="Return",size_hint=(1,.1))
        gl.add_widget(bw)
        bw.bind(on_press=self.app.return_screen)

    def set_config(self, config):
        self.settings = SettingsWithNoMenu(text_size="30")
        self.settings.add_json_panel('Pente', config, 'pente.json')

    def on_enter(self):
        if self.settings.parent is None:
            self.build()

    def on_leave(self, ignored=None):
        self.app.set_confirmation_popups()

