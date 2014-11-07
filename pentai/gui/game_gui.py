"""
This is for keeping the one current game in the GUI
"""
from pentai.base.defines import *

_game_instance = None

def get_instance():
    return _game_instance

def set_instance(the_game):
    global _game_instance
    _game_instance = the_game
