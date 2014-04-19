from kivy.uix.screenmanager import Screen

from pentai.base.defines import *
import scale

class IntroScreen(Screen):
    def __init__(self, *args, **kwargs):

        super(IntroScreen, self).__init__(*args, **kwargs)

    def on_enter(self):
        # TODO: Fancy graphics, transition to menu
        pass

