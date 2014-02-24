import kivy
kivy.require('1.0.8')

from kivy.core.audio import SoundLoader
import glob as g_m
from os.path import dirname, join, basename
import random as r_m
from defines import *

instance = None

class Audio():
# Sound effects: place, capture, tick, win, loss, music
    def __init__(self, config):
        self.config = config
        self.sound_cache = {}
        self.filenames_cache = {}
        self.last_played = {}
        self.muted = False

        global instance
        instance = self

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False

    def play_sound(self, file_paths):
        if self.muted:
            return
        
        fn_in_subdir = join("media", *file_paths)
        # Avoid doing the glob every time
        try:
            filenames = self.filenames_cache[fn_in_subdir][:]
            last_played = self.last_played[fn_in_subdir]
            if len(filenames) > 1:
                filenames.remove(last_played)
        except KeyError:
            self.filenames_cache[fn_in_subdir] = filenames \
                = g_m.glob("%s*.wav" % fn_in_subdir)

        filename = r_m.choice(filenames)
        self.last_played[fn_in_subdir] = filename

        # Avoid loading the sound every time
        try:
            sound = self.sound_cache[filename]
        except KeyError:
            self.sound_cache[filename] = sound = SoundLoader.load(filename)

        # stop the sound if it's currently playing
        if sound.status != 'stop':
            sound.stop()
        vol = self.config.get("PentAI", "effects_volume")
        sound.volume = float(vol)
        sound.play()

    def place(self):
        self.play_sound(["stones", "place"])
    
    def capture(self, ignored=None):
        self.play_sound(["stones", "capture"])

    def tick(self):
        # TODO
        pass
        #self.play_sound(["tick", "tick"])
        self.play_sound(["click", "click"])

    def win(self):
        self.play_sound(["win", "win"])

    def lose(self):
        self.play_sound(["lose", "lose"])

    def beep(self):
        self.play_sound(["beep", "beep"])

    def click(self):
        self.play_sound(["click", "click"])

    def music(self):
        pass

