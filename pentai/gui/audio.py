import kivy
kivy.require('1.0.8')

from kivy.core.audio import SoundLoader
from kivy.clock import Clock

import glob as g_m
import random
from os.path import dirname, join, basename

import pentai.base.logger as log

instance = None

class Audio():
    """ Sound effects: place, capture, tick, win, loss, music """
    def __init__(self, config):
        self.config = config
        self.sound_cache = {}
        self.filenames_cache = {}
        self.last_played = {}
        self.muted = False
        self.demo_volume = 1.0
        self.current_music_sound = None
        self.game_over_sound = None

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

        vol = self.config.getfloat("PentAI", "effects_volume")
        sound.volume = self.demo_volume * vol
        sound.play()
        return sound

    def place(self):
        self.play_sound(["stones", "place"])
    
    def capture(self, ignored=None):
        self.play_sound(["stones", "capture"])

    def tick(self, colour):
        if self.config.getint("PentAI", "tick"):
            fn = "tick%s" % "nBW"[colour]
            self.play_sound(["tick", fn])

    def win(self):
        if self.config.getint("PentAI", "win_loss_sound"):
            self.game_over_sound = self.play_sound(["win", "win"])

    def lose(self):
        if self.config.getint("PentAI", "win_loss_sound"):
            self.game_over_sound = self.play_sound(["lose", "lose"])

    def hush_game_over_sound(self):
        try:
            self.game_over_sound.stop()
        except AttributeError:
            pass
        self.game_over_sound = None

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

        vol = self.config.getfloat("PentAI", "effects_volume")
        self.current_demo_sound.volume = vol
        self.current_demo_sound.play()
    
    def adjust_music_volume(self):
        vol = self.config.getfloat("PentAI", "music_volume")
        log.debug("adjust_music_volume %s" % vol)
        if vol < .01:
            log.debug("adjust_music_volume stopping track")
            try:
                self.current_music_sound.stop()
                self.current_music_sound = None
                Clock.unschedule(self.schedule_music)
            except AttributeError:
                pass
        elif self.current_music_sound == None:
            self.schedule_music()
        if self.current_music_sound:
            self.current_music_sound.volume = vol * self.demo_volume

    def inc_piece_number(self):
        try:
            self.piece_number += 1
        except AttributeError:
            # Choose a random piece to start at.
            self.piece_number = random.randrange(0, 13)
        return self.piece_number

    def reset_piece_number(self):
        self.piece_number = 1

    def play_music(self, *ignored):
        if self.muted:
            return

        cms = self.current_music_sound
        if cms and cms.state == "play":
            return

        vol = self.config.get("PentAI", "music_volume")

        while True:
            try:
                pn = self.inc_piece_number()
            except:
                pn = self.reset_piece_number()

            music_file_pattern = join("media", "music", str(pn))
            filenames = g_m.glob("%s.*.ogg" % music_file_pattern)
            try:
                filename = filenames[0] # Should be only 1 track per track num.
                self.current_track_name = filename.split('.')[1]
                # Found one, quit looping
                break
            except IndexError:
                # Loop back to first piece
                pn = self.reset_piece_number()

        self.current_music_sound = SoundLoader.load(filename)

        self.adjust_music_volume()
        try:
            self.current_music_sound.play()
        except AttributeError:
            pass

    def schedule_music(self, *ignored):
        self.current_music_sound = None
        self.play_music()
        if self.current_music_sound:
            track_length = self.current_music_sound.length
            log.debug("track_length: %s" % track_length)
            if track_length > 10000:
                # Work around for Kivy problem.
                track_length /= 10980
                log.debug("Adjusted track_length: %s" % track_length)
            Clock.schedule_once(self.schedule_music, track_length + 0.5)

    def get_current_track_name(self):
        return self.current_track_name

def adjust_volumes():
    instance.adjust_music_volume()


