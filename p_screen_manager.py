from kivy.uix.screenmanager import *

import random

class PScreenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.demo = None
        super(PScreenManager, self).__init__(*args, **kwargs)

    def set_demo(self, d):
        self.demo = d 

    def set_current(self, screen_name):
        self.random_transition()
        if self.current != screen_name:
            self.current = screen_name

    def random_transition(self):
        # The other transition types trigger a crash
        trans = self.transition = SlideTransition()

        dirs = ['right','up','down','left']
        try:
            dirs.remove(self.last_choice)
        except: pass
        dc = random.choice(dirs)
        self.last_choice = dc
        trans.direction = dc

    def in_demo_mode(self):
        return self.demo != None

    def on_touch_down(self, *args, **kwargs):
        if self.in_demo_mode():
            self.demo.interrupt()
        else:
            return super(PScreenManager, self).on_touch_down(*args, **kwargs)
    
    def on_touch_move(self, *args, **kwargs):
        if self.in_demo_mode():
            pass
        else:
            return super(PScreenManager, self).on_touch_move(*args, **kwargs)
    
    def on_touch_up(self, *args, **kwargs):
        if self.in_demo_mode():
            pass
        else:
            return super(PScreenManager, self).on_touch_up(*args, **kwargs)

    def leave(self):
        self.current_screen.on_leave()
    
