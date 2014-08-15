from kivy.uix.screenmanager import Screen

from my_setting import *
import audio as a_m

from kivy.uix.widget import Widget

# TODO: Spacers could live elsewhere
class HSpacer(Widget):
    pass

class VSpacer(Widget):
    pass

class SettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)
        self.ids.build_id.bind(value=self.on_build_ob)                  

    def adjust_volumes(self, *args):
        a_m.adjust_volumes()

    def set_confirmation_popups(self, *args):
        self.app.set_confirmation_popups()

    def on_build_ob(self, widget, val, *args):
        if val == "Build All Now":
            print val

