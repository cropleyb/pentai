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


class SettingsScreen(Screen):
    show_moves = BooleanProperty(True)
    show_captures = BooleanProperty(True)
    require_captures = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)

