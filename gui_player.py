
from kivy.clock import Clock

import audio as a_m
from defines import *

class GuiPlayer(object):
    def __init__(self, player, widget):
        self.player = player
        self.widget = widget
        total_time = player.get_total_time()
        self.total_time = total_time
        self.audio_remaining_time = total_time
        self.video_remaining_time = total_time
        self.audio_queued_tick = None

    def prompt_for_move(self, colour):
        # Start visual and audio timers
        if self.audio_queued_tick == None:
            self.tick_audio(0, colour)
            self.tick_video(0)

    def make_move(self):
        # Stop both timers
        if self.audio_queued_tick:
            # TODO: subtract fraction of a second already spent
            self.audio_queued_tick.cancel()
            self.video_queued_tick.cancel()

        self.audio_queued_tick = None

    def tick_audio(self, dt, colour=None):
        if colour is None:
            colour = self.last_colour
        else:
            self.last_colour = colour
        a_m.instance.tick(colour)
        self.audio_remaining_time -= dt

        tt = self.total_time
        rem = self.audio_remaining_time

        if rem > 0:
            interval = (.5 * (1 + (rem / tt))) ** 2
            self.audio_queued_tick = \
                Clock.schedule_once(self.tick_audio, interval)

    def tick_video(self, dt):
        self.video_remaining_time -= 1

        rem = self.video_remaining_time

        self.widget.text = "%s:%02d" % (rem/60, rem%60)

        if rem > 0:
            self.video_queued_tick = Clock.schedule_once(self.tick_video, 1)

