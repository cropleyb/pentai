from kivy.uix.screenmanager import Screen

from pentai.gui.spacer import *
from pentai.gui.scrollable_label import *

class HelpScreen(Screen):
    def on_pre_enter(self):
        self.set_text()

