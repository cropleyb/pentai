import kivy
kivy.require('1.0.8')

from kivy.core.audio import SoundLoader
import glob as g_m
from os.path import dirname, join, basename
import random as r_m
from defines import *

class Audio():
# Sound effects: place, capture, tick, win, loss, music
    def __init__(self, config):
        self.config = config
        self.sound_cache = {}
        self.filenames_cache = {}
        self.muted = False

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
            filenames = self.filenames_cache[fn_in_subdir]
        except KeyError:
            self.filenames_cache[fn_in_subdir] = filenames \
                = g_m.glob("%s*.wav" % fn_in_subdir)

        filename = r_m.choice(filenames)

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
        pass

    def win(self):
        self.play_sound(["win", "win"])

    def lose(self):
        self.play_sound(["lose", "lose"])

    def beep(self):
        self.play_sound(["beep", "beep"])

    def music(self):
        pass

'''
def make_noise():
    sound = SoundLoader.load("12919_sweet_trip_mm_kwik_mod_04.wav")
    # stop the sound if it's currently playing
    if sound.status != 'stop':
        sound.stop()
    sound.play()

class AudioButton(Button):

    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)

    def on_press(self):
        if self.sound is None:
            self.sound = SoundLoader.load(self.filename)
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.play()

    def release_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None


class AudioBackground(BoxLayout):
    pass


class AudioApp(App):

    def build(self):

        root = AudioBackground(spacing=5)
        for fn in glob(join(dirname(__file__), '*.wav')):
        #for fn in glob(join(dirname(__file__), '*.mp3')):
            btn = AudioButton(
                text=basename(fn[:-4]).replace('_', ' '), filename=fn,
                size_hint=(None, None), halign='center',
                size=(128, 128), text_size=(118, None))
            root.ids.sl.add_widget(btn)

        return root

    def release_audio(self):
        for audiobutton in self.root.ids.sl.children:
            audiobutton.release_audio()

if __name__ == '__main__':
    AudioApp().run()
'''
