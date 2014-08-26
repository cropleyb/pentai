from kivy.uix.screenmanager import Screen

from my_setting import *
import audio as a_m

from popup import *

'''
BUILD_ALL_NOW = "Build All Now"
BUILT = "Built"
DONT_BUILD = "Don't Build"
PART_ON_STARTUP = "Part On Startup"
'''

class SettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SettingsScreen, self).__init__(*args, **kwargs)
        #self.build_spinner = self.ids.build_id
        #self.build_spinner.bind(value=self.on_build_ob)                  
        self.app = None

    '''
    def on_pre_enter(self):
        self.set_build_options()

    def set_build_options(self):
        try:
            if self.app.openings_book_is_finished():
                self.build_spinner.set_desc("The openings book has been built")
                self.build_spinner.set_values((BUILT,))
                self.ids.build_id.save_value(None, BUILT)
                self.ids.build_id.load_value()
                return
        except AttributeError:
            pass
        self.build_spinner.set_desc("Do you want to use the openings book?")
        self.build_spinner.set_values((DONT_BUILD, PART_ON_STARTUP, BUILD_ALL_NOW))
        val = self.ids.build_id.load_value()
        if val == BUILT:
            self.ids.build_id.save_value(None, DONT_BUILD)
            self.ids.build_id.load_value()
    '''

    def adjust_volumes(self, *args):
        a_m.adjust_volumes()

    def set_confirmation_popups(self, *args):
        self.app.set_confirmation_popups()

    '''
    def on_build_ob(self, widget, val, *args):
        if val == BUILD_ALL_NOW:
            msg_str = "Build entire DB now?"
            ConfirmPopup.create_and_open(message=msg_str,
                        action=self.on_build_ob_inner,
                        size_hint=(.8, .2))

    def on_build_ob_inner(self, *args):
        self.app.build_all_openings()
        self.ids.build_id.save_value(None, PART_ON_STARTUP)
        self.ids.build_id.load_value()
    '''
