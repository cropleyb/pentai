
from kivy.clock import Clock

import audio as a_m
from defines import *

class GuiPlayer(object):
    def __init__(self, player, widget, game):
        self.player = player
        self.widget = widget
        self.game = game
        total_time = game.get_total_time()
        self.total_time = total_time
        self.audio_remaining_time = total_time
        self.show_remaining()
        self.ticking = False

    def prompt_for_move(self, colour):
        if not self.ticking:
            self.tick_audio(0, colour)
            self.tick_video(0)
            self.ticking = True

    def make_move(self):
        # Stop both timers
        Clock.unschedule(self.tick_audio)
        Clock.unschedule(self.tick_video)
        self.ticking = False

    def tick_audio(self, dt, colour=None):
        if colour is None:
            colour = self.last_colour
        else:
            self.last_colour = colour
        if dt > 0:
            a_m.instance.tick(colour)
            self.audio_remaining_time -= dt

        tt = self.total_time
        rem = self.audio_remaining_time

        if rem > 0:
            interval = (.5 * (1 + (rem / tt))) ** 2
            Clock.schedule_once(self.tick_audio, interval)

    def tick_video(self, dt):
        rem = self.player.tick(dt)
        next_tick_time = rem % 1.0

        self.show_remaining()

        if rem > 0:
            Clock.schedule_once(self.tick_video, next_tick_time)
        else:
            other_colour = opposite_colour(self.game.to_move_colour())
            self.game.set_won_by(other_colour)

    def show_remaining(self):
        rem = round(self.player.remaining_time)
        self.widget.text = "%2d:%02d" % (rem/60, rem%60)
