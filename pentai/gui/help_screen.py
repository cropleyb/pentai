from pentai.gui.screen import Screen

from pentai.gui.spacer import *
from pentai.gui.scrollable_label import *
from pentai.gui.section import *

from kivy.clock import Clock

class HelpScreen(Screen):
    def on_pre_enter(self):
        self.set_text()

class NewHelpScreen(Screen):
    title_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(NewHelpScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.setup_text, 0.5)

    def setup_text(self, *ignored):
        self.title_text = self.title
        scrolled = self.ids.scrollable_id
        scrolled.add_widget(self.help_text_class())

class HelpText(MyScrollable):
    pass
