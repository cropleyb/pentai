
import os

def get_font_path(font_name):
    font_path = os.path.join("media", "fonts", "%s.ttf" % font_name)
    return font_path

def get_all_font_paths():
    global AI_FONT
    AI_FONT = get_font_path("Courier")

import re

def conv(orig_string):
    out = re.sub("\[AI\]", "[font=%s][color=ffaaaaff]" % AI_FONT, orig_string)
    out = re.sub("\[/AI\]", "[/color][/font]", out)
    out = re.sub(r"\[REF=(\w+)\]", r"[ref=\1][color=00eeeeff]", out)
    out = re.sub("\[/REF\]", "[/color][/ref]", out)
    return out

get_all_font_paths()

