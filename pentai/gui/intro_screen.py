from pentai.gui.screen import Screen
import kivy.uix.gridlayout as gl_m
import kivy.uix.label as l_m
import kivy.uix.progressbar as pb_m
from kivy.clock import Clock

import scale as my
import random

class IntroScreen(Screen):
    def __init__(self, *args, **kwargs):

        super(IntroScreen, self).__init__(*args, **kwargs)

        self.activity_label = self.ids.activity_label_id
        self.progress_bar = self.ids.progress_bar_id
        
        self.show_activity()

    def on_enter(self):
        Clock.schedule_once(self.add_progress, .5)

    def on_leave(self):
        Clock.unschedule(self.add_progress)

    def prompt_quit(self):
        self.app.prompt_quit()

    def pop_screen(self):
        self.app.interrupt_openings_building()
        self.app.pop_screen()

    def show_help(self):
        self.app.show_intro_help()

    def add_progress(self, *ignored):
        self.progress_bar.value += random.randrange(50, 150)
        if self.progress_bar.value >= 1000:
            self.progress_bar.value = 0
            self.show_activity()
        Clock.schedule_once(self.add_progress, .2 + 1 * random.random())

    activity_list = [
        "Unpacking board", "Polishing stones", "Brushing teeth", "Arranging furniture", "Winding clocks", "Getting snacks", "Putting kids to bed", "Putting cat out", "Adjusting central heating", "Sound check", "Getting a drink", "Call of nature", "Preparing distractions", "Answering phone", "Texting workmate", "Putting away dishes", "Reading the paper", "Paying bills", "Gathering audience", "Placing wagers", "Practicing openings", "Gossiping with neighbours", "Procrastinating", "Boasting about previous games", "Anticipating", "Watching an ad", "Watering pot-plants", "Online shopping", "Grazed knee", "Complaining", "None of your business", "Composing oneself", "Nothing much", "CPR on Aunt Mabel", "Finishing meal", "Toasting marshmallows", "Biting nails", "Scratching", "(censored)", "Changing footwear", "You don't want to know", "Attending to personal hygene", "Is it alive?", "Contributing to Global Warming", "Meditating", "Packing"
        ]

    def show_activity(self, *ignored):
        self.progress_bar.value = 0
        prev = self.activity_label.text
        while self.activity_label.text == prev:
            self.activity_label.text = random.choice(self.activity_list)

