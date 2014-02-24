
from kivy.clock import Clock

import audio as a_m

class GuiPlayer(object):
    def __init__(self, total_time):
        self.total_time = total_time
        self.remaining_time = total_time

    def prompt_for_move(self):
        # Start visual and audio timers
        self.tick(0)

    def tick(self, dt):
        a_m.instance.tick()
        self.remaining_time -= dt

        tt = self.total_time
        rem = self.remaining_time

        if rem > 0:
            interval = (.5 * (1 + (rem / tt))) ** 2
            self.queued_tick = Clock.schedule_once(self.tick, interval)

    def make_move(self):
        # Stop both timers
        self.queued_tick.cancel()
