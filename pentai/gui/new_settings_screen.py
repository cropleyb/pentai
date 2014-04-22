from kivy.uix.screenmanager import Screen
from kivy.properties import *

from my_setting import *
import audio as a_m

class NewSettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(NewSettingsScreen, self).__init__(*args, **kwargs)

    def adjust_volumes(self, *args):
        a_m.adjust_volumes()

