from kivy.uix.screenmanager import Screen
import kivy.uix.gridlayout as gl_m
import kivy.uix.label as l_m

from pentai.base.defines import *
import scale

class IntroScreen(Screen):
    def __init__(self, *args, **kwargs):

        super(IntroScreen, self).__init__(*args, **kwargs)

        gl = gl_m.GridLayout()
        gl.cols = 1
        self.add_widget(gl)

        l = l_m.Label()
        l.size_hint = (1, 0.1)
        l.text = "PentAI is loading..."
        gl.add_widget(l)

    def on_enter(self):
        # TODO: Fancy graphics, transition to menu
        pass

