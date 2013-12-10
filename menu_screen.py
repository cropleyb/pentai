from kivy.uix.screenmanager import Screen
from kivy.properties import *

class MenuScreen(Screen):
    show_moves = BooleanProperty(True)
    show_captures = BooleanProperty(True)
    require_captures = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)

