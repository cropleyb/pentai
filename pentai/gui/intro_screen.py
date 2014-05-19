from kivy.uix.screenmanager import Screen
import kivy.uix.gridlayout as gl_m
import kivy.uix.label as l_m
import kivy.uix.progressbar as pb_m
from kivy.clock import Clock

from pentai.base.defines import *
import scale as my
import random

class IntroScreen(Screen):
    def __init__(self, *args, **kwargs):

        super(IntroScreen, self).__init__(*args, **kwargs)

        gl = gl_m.GridLayout()
        gl.cols = 1
        self.add_widget(gl)

        l = l_m.Label()
        l.size_hint = (1, 0.1)
        l.text = "Preparing for PentAI!"
        l.font_size = my.dp(40)
        gl.add_widget(l)

        self.activity_label = l2 = l_m.Label()
        l2.size_hint = (1, 0.1)
        l2.font_size = my.dp(30)
        gl.add_widget(l2)

        self.progress_bar = pb = pb_m.ProgressBar(max=1000)
        pb.size_hint = (1, 0.1)
        gl.add_widget(pb)
        
        self.show_activity()

    def on_enter(self):
        # TODO: Fancy graphics, transition to menu
        Clock.schedule_interval(self.show_activity, 5)
        Clock.schedule_interval(self.add_dot, .5)

    def on_leave(self):
        Clock.unschedule(self.show_activity)
        Clock.unschedule(self.add_dot)

    def add_dot(self, *ignored):
        self.progress_bar.value += 100
        #self.activity_label.text = self.activity_label.text + "."

    activity_list = [
        "Unpacking board", "Polishing stones", "Brushing teeth", "Arranging furniture", "Winding clocks", "Getting snacks", "Putting kids to bed", "Putting cat out", "Adjusting central heating", "Sound check", "Getting a drink", "Call of nature", "Preparing distractions", "Answering phone", "Texting workmate", "Putting away dishes", "Reading the paper", "Paying bills", "Gathering audience", "Placing wagers", "Practicing openings", "Gossiping with neighbours", "Procrastinating", "Boasting about previous games", "Anticipating", "Watching an ad", "Watering pot-plants", "Online shopping", "Grazed knee", "Complaining"
        ]

    def show_activity(self, *ignored):
        self.progress_bar.value = 0
        prev = self.activity_label.text
        while self.activity_label.text == prev:
            self.activity_label.text = random.choice(self.activity_list)

