import kivy
kivy.require('1.0.8')

from kivy.core.audio import SoundLoader
from kivy.clock import Clock

import glob as g_m
from os.path import dirname, join, basename
import random
from pentai.db.misc_db import get_instance as m_m

instance = None

PN_KEY = "piece_number"

class Audio():
# Sound effects: place, capture, tick, win, loss, music
    def __init__(self, config):
        self.config = config
        self.sound_cache = {}
        self.filenames_cache = {}
        self.last_played = {}
        self.muted = False
        self.demo_volume = 1.0

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
            filenames = g_m.glob("%s*.wav" % fn_in_subdir)
            filenames.extend(g_m.glob("%s*.ogg" % fn_in_subdir))
            self.filenames_cache[fn_in_subdir] = filenames

        filename = random.choice(filenames)
        self.last_played[fn_in_subdir] = filename

        # Avoid loading the sound every time
        try:
            sound = self.sound_cache[filename]
        except KeyError:
            self.sound_cache[filename] = sound = SoundLoader.load(filename)

        # stop the sound if it's currently playing
        if sound.status != 'stop':
            sound.stop()

        vol = float(self.config.get("PentAI", "effects_volume"))
        sound.volume = self.demo_volume * vol
        sound.play()

    def place(self):
        self.play_sound(["stones", "place"])
    
    def capture(self, ignored=None):
        self.play_sound(["stones", "capture"])

    def tick(self, colour):
        if self.config.getint("PentAI", "tick"):
            fn = "tick%s" % "nBW"[colour]
            self.play_sound(["tick", fn])

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

    def start_demo(self):
        self.demo_volume = .3

    def cut_demo(self):
        self.current_demo_sound.stop()
        self.demo_volume = 1
        self.adjust_music_volume()

    def demo(self, part):
        if self.muted:
            return
        
        self.adjust_music_volume()
        fn_in_subdir = join("media", "demo", "%s.ogg" % part)

        try:
            self.current_demo_sound.stop()
        except: pass
        self.current_demo_sound = SoundLoader.load(fn_in_subdir)

        vol = self.config.get("PentAI", "effects_volume")
        self.current_demo_sound.volume = float(vol)
        self.current_demo_sound.play()

    def adjust_music_volume(self):
        vol = self.config.get("PentAI", "music_volume")
        self.current_music_sound.volume = float(vol) * self.demo_volume

    def inc_piece_number(self):
        m_m()[PN_KEY] += 1
        return m_m()[PN_KEY]

    def reset_piece_number(self):
        pn = m_m()[PN_KEY] = 1
        return pn

    def play_music(self, *ignored):
        if self.muted:
            return
        vol = self.config.get("PentAI", "music_volume")

        while True:
            try:
                pn = self.inc_piece_number()
            except:
                # For initial value of 1
                pn = self.reset_piece_number()

            music_file_pattern = join("media", "music", str(pn))
            filenames = g_m.glob("%s.*.ogg" % music_file_pattern)
            try:
                filename = filenames[0] # Should be 1
                # Found one, quit looping
                break
            except IndexError:
                # Loop back to first piece
                pn = self.reset_piece_number()

        self.current_music_sound = SoundLoader.load(filename)

        self.adjust_music_volume()
        self.current_music_sound.play()
        Clock.schedule_once(self.play_music, self.current_music_sound.length + 3.0)

def adjust_volumes():
    instance.adjust_music_volume()


