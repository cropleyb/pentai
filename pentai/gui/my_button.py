
from kivy.uix.button import Button
import audio as a_m
from pentai.base.defines import *

class MyButton(Button):
    def __init__(self, *args, **kwargs):
        super(MyButton, self).__init__(*args, **kwargs)
        self.silent = False

    def on_touch_up(self, touch, *args, **kwargs):
        if self.collide_point(*touch.pos):
            if not self.silent:
                a_m.instance.click()
        super(MyButton, self).on_touch_up(touch, *args, **kwargs)

    def sim_press(self):
        self.state = "down"

    def sim_release(self, ignored=None):
        self.state = "normal"
        if not self.silent:
            a_m.instance.click()


