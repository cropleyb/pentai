
import os
from kivy.uix.label import *
from kivy.properties import StringProperty # Is this necessary?

def get_font_path(font_name):
    font_path = os.path.join("media", "fonts", "%s.ttf" % font_name)
    return font_path

def get_all_font_paths():
    global AI_FONT
    AI_FONT = get_font_path("Courier Prime Bold")

    #Label.font_name = StringProperty(fonts["Courier Prime"])

get_all_font_paths()

