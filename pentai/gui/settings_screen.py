from kivy.uix.screenmanager import Screen
#from kivy.properties import *
from kivy.uix.settings import SettingSpacer

from my_setting import *
import audio as a_m

class SettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)

    def adjust_volumes(self, *args):
        a_m.adjust_volumes()

    def set_confirmation_popups(self, *args):
        self.app.set_confirmation_popups()

