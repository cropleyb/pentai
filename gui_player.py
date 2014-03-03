
from kivy.clock import Clock

import audio as a_m
from defines import *

class GuiPlayer(object):
    def __init__(self, colour, widget, game):
        self.colour = colour
        self.player = game.get_player(colour)
        self.widget = widget
        self.game = game
        total_time = game.get_total_time()
        self.total_time = total_time
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
            # Make tick sound
            a_m.instance.tick(colour)

        tt = self.total_time
        rem = self.game.remaining_time(self.colour)

        if rem > 0:
            interval = (.5 * (1 + (rem / tt))) ** 2
            Clock.schedule_once(self.tick_audio, interval)

    def tick_video(self, dt):
        rem = self.game.tick(self.colour, dt)
        next_tick_time = rem % 1.0

        self.show_remaining()

        if rem > 0:
            Clock.schedule_once(self.tick_video, next_tick_time)
        else:
            other_colour = opposite_colour(self.game.to_move_colour())

    def refresh(self):
        self.show_remaining()

    def show_remaining(self):
        rem = round(self.game.remaining_time(self.colour))
        self.widget.text = "%2d:%02d" % (rem/60, rem%60)
