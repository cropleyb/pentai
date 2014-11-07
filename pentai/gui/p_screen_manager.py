from kivy.uix.screenmanager import *

from pentai.gui.intro_screen import *
from pentai.gui.intro_help_screen import *
from pentai.base.defines import *
from pentai.base.future import *
from pentai.gui.guide import *
import pentai.base.logger as log

import importlib
import random

from pentai.gui.setup_screen import *
from pentai.gui.pente_screen import *

class PScreenManager(ScreenManager):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.demo = None
        super(PScreenManager, self).__init__(*args, **kwargs)
        self.transition = SlideTransition()
        self.random_transition()
        self.previous = []
        # self.guide = Guide() # TODO: Persistent -> misc_db

    def push_demo(self, d):
        self.previous.append(self.current)
        self.set_demo(d)

    def set_demo(self, d):
        if self.demo:
            self.demo.clean_up()
        self.demo = d 

    def push_current(self, screen_name):
        if self.current == screen_name:
            return
        log.debug("Pushing %s to %s, change to %s" % (self.current, self.previous, screen_name))
        self.previous.append(self.current)
        self.set_current(screen_name)
        if len(self.previous) > 20:
            self.previous[:1] = []

    def get_size(self):
        return self.current_screen.size

    def resize(self, *args):
        pente_screen = None
        current = self.current
        if current == "Pente":
            # Only resize PenteScreen if it is the current screen,
            # otherwise just create a new one.
            pente_screen = self.get_screen("Pente")
            pente_screen.resize(args[1:])

        self.clear_widgets()

        if pente_screen:
            try:
                self.add_widget(pente_screen)
            except ScreenManagerException:
                pass
        self.set_current(current)

    def set_current(self, screen_name):
        if self.current != screen_name:
            self.leave()
            self.random_transition()
            self.create_if_necessary(screen_name)
            self.current = screen_name
            if not self.in_demo_mode():
                if screen_name:
                    self.guide.on_enter(screen_name)

    def get_screen(self, screen_name, init=True):
        if init:
            self.create_if_necessary(screen_name)
        try:
            return super(PScreenManager, self).get_screen(screen_name)
        except ScreenManagerException:
            return None

    def pop_screen(self):
        log.debug("Popping to %s" % (self.previous))
        if len(self.previous) < 1:
            return False

        self.set_current(self.previous[-1])
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
        self.guide.on_leave()

    def create_if_necessary(self, screen_name):
        if screen_name != "Pente" and not self.has_screen(screen_name):
            scr_mod_name, scr_cls_name = self.screen_data[screen_name]
            scr_mod = "pentai.gui.%s_screen" % scr_mod_name

            mod = importlib.import_module(scr_mod)
            scr_cls_name = "%sScreen" % (scr_cls_name,)
            scr_cls = getattr(mod, scr_cls_name)

            self.add_screen_inc_globals(scr_cls, screen_name)

    
    def add_screen(self, scr_cls, scr_name):
        scr = scr_cls(name=scr_name)
        scr.set_app(self.app)
        scr.set_config(self.app.config)
        self.add_widget(scr)
        return scr

    def add_screen_inc_globals(self, scr_cls, scr_name):
        scr = self.add_screen(scr_cls, scr_name)
        app = self.app
        scr.set_games_mgr(app.games_mgr)
        scr.set_openings_book(app.openings_book)
        scr.set_players_mgr(app.games_mgr.players_mgr)
        return scr

    screen_data = {
            "Menu": ("menu", "Menu"),
            "Settings": ("settings", "Settings"),
            "SettingsHelp": ("settings_help", "SettingsHelp", ),
            "Setup": ("setup", "Setup", ),
            "GameSetupHelp": ("setup_help", "SetupHelp", ),
            "Load": ("games", "Games", ),
            "LoadHelp": ("load_help", "LoadHelp", ),
            "AI": ("ai_player", "AIPlayer", ),
            "AIHelp": ("ai_help", "AIHelp", ),
            "Human": ("human_player", "HumanPlayer", ),
            "HumanHelp": ("human_help", "HumanHelp", ),
            "PenteHelp": ("pente_help", "PenteHelp", ),
            "GoodBye": ("goodbye", "GoodBye", ),
           }

