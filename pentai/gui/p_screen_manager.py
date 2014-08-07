from kivy.uix.screenmanager import *

import pentai.gui.intro_screen as i_m
from pentai.base.defines import *

import random

class PScreenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.demo = None
        super(PScreenManager, self).__init__(*args, **kwargs)
        self.transition = SlideTransition()
        self.random_transition()
        self.previous = []

    def set_demo(self, d):
        if self.demo:
            self.demo.clean_up()
        self.demo = d 

    def show_intro_screen(self):
        self.add_widget(i_m.IntroScreen(name="Intro"))
        self.current = "Intro"

    def push_current(self, screen_name):
        self.previous.append(self.current)
        self.set_current(screen_name)
        if len(self.previous) > 4:
            self.previous[:2] = []

    def set_current(self, screen_name):
        if self.current != screen_name:
            self.random_transition()
            self.current = screen_name

    def return_screen(self):
        self.current = self.previous[-1]
        del self.previous[-1]

    def clear_hist(self):
        self.previous[:] = []

    def random_transition(self):
        trans = self.transition

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
    
