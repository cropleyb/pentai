from kivy.uix.screenmanager import *

from pentai.gui.intro_screen import *
from pentai.gui.intro_help_screen import *
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

    def push_current(self, screen_name):
        self.previous.append(self.current)
        self.set_current(screen_name)
        if len(self.previous) > 6:
            self.previous[:1] = []

    def set_current(self, screen_name):
        if self.current != screen_name:
            self.random_transition()
            self.current = screen_name

    def pop_screen(self):
        if len(self.previous) <= 1:
            return False

        self.current = self.previous[-1]
        del self.previous[-1]
        return True

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
    
    def get_all_screens(self):
        import menu_screen as ms_m
        import ai_player_screen as aips_m
        import ai_help_screen as aihs_m
        import human_player_screen as hps_m
        import human_help_screen as hhs_m
        import setup_screen as sts_m
        import setup_help_screen as shs_m
        import settings_screen as ses_m
        import settings_help_screen as sehs_m
        import games_screen as gs_m
        import load_help_screen as lhs_m

        screens = [(ms_m.MenuScreen, "Menu"),
                   (ses_m.SettingsScreen, "Settings"),
                   (sehs_m.SettingsHelpScreen, "SettingsHelp"),
                   (sts_m.SetupScreen, "Setup"),
                   (shs_m.SetupHelpScreen, "GameSetupHelp"),
                   (gs_m.GamesScreen, "Load"),
                   (lhs_m.LoadHelpScreen, "LoadHelp"),
                   (aips_m.AIPlayerScreen, "AI"), (aihs_m.AIHelpScreen, "AIHelp"),
                   (hps_m.HumanPlayerScreen, "Human"), (hhs_m.HumanHelpScreen, "HumanHelp"),
                   ]
        return screens
