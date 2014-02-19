from kivy.app import App
from kivy.config import Config
from kivy.clock import *
from kivy.base import *
#from kivy.core.window import Window # Hmmmm... TODO?

from kivy.config import ConfigParser
from kivy.uix.settings import Settings

from kivy.uix.screenmanager import * # TODO: Remove

import p_screen_manager as ps_m

from ai_player_screen import *
from setup_screen import *
from settings_screen import *
from pente_screen import *
from menu_screen import *
from games_screen import *

from popup import *
import my_button
from games_mgr import *
import openings_book as ob_m

from kivy.properties import ObjectProperty

import alpha_beta as ab_m
import os # TODO: Remove?
import time
import ai_player as aip_m # hack for debugging
import random

import copy as c_m
import demo as d_m
import misc_db

class PentAIApp(App):
    game_filename = StringProperty("")

    def display_error(self, message):
        self.popup = MessagePopup(title='Error', content=Label(text=message, font_size='20sp'), \
                size_hint=(.8, .2))
        self.popup.open()
        print message

    def return_screen(self, ignored=None):
        if self.pente_screen:
            self.show_pente_screen()
        else:
            self.show_menu_screen()

    def show_settings_screen(self):
        self.random_transition()
        self.root.current = "Settings"

    def show_pente_screen(self):
        self.random_transition()
        self.root.current = "Pente"

    def show_games_screen(self, ignored=None):
        self.random_transition()
        self.root.current = "Games"

    def show_ai_screen(self, ignored=None):
        self.random_transition()
        self.root.current = "AI"

    def show_menu_screen(self, ignored=None):
        self.random_transition()
        self.root.current = "Menu"

    def show_new_game_screen(self):
        self.random_transition()
        self.game_filename = ""
        self.setup_screen.create_game()
        self.root.current = "Setup"

    def show_demo(self):
        d = d_m.Demo(self, self.setup_screen.size)

        # Intercept all touch events
        self.root.set_demo(d)

        for db_inst in [self.games_mgr, self.openings_book, misc_db.get_instance()]:
            # Deep copy and save.
            # (Players are in games_mgr)
            orig = db_inst.__dict__
            db_inst.__dict__ = c_m.deepcopy(db_inst.__dict__)
            db_inst._backup = orig

        d.start()

    def finish_demo(self):
        self.show_menu_screen()
        self.pente_screen = None
        self.root.set_demo(None)
        Clock.schedule_once(self.restore_from_demo, .1)

    def restore_from_demo(self, *ignored):
        for db_inst in [self.games_mgr, self.openings_book, misc_db.get_instance()]:
            # Restore each to backup
            db_inst.__dict__ = db_inst._backup

    def load_game_file_cb(self, path, filenames):
        f_n = filenames
        try:
            full_path = os.path.join(path, filenames[0])
        except IndexError:
            self.display_error("Please select a game first")
            return
        self.load_game_file(full_path)

    def edit_game(self, game=None):
        if not game is None:
            self.game = game
        self.setup_screen.alter_game(self.game)
        self.root.current = "Setup"

    def load_game_file(self, full_path=None):
        if full_path != None:
            self.game_filename = full_path
        if self.game_filename == "":
            self.game_filename = self.game.autosave_filename
        # TODO: Check file parsed etc.
        self.setup_screen.load_file(self.game_filename)
        # TODO production app should start game here.
        self.root.current = "Setup"

    def start_game(self, game, screen_size, demo=False):
        # TODO: Move this?
        root = self.root
        try:
            prev_game_screen = root.get_screen("Pente")
            if prev_game_screen != None:
                root.remove_widget(prev_game_screen)
        except ScreenManagerException:
            pass

        self.add_screen(PenteScreen,
            'Pente', screen_size=screen_size,
            filename=self.game_filename)

        self.pente_screen = root.get_screen("Pente")
        self.pente_screen.set_live(not demo)
        self.game = game

        # load the game screen
        self.pente_screen.set_game(game)

        self.show_pente_screen()

    def prompt_quit(self):
        msg_str = "Are you sure you want to quit?"
        ConfirmPopup.create_and_open(message=msg_str,
                    action=self.close_confirmed,
                    size_hint=(.8, .2))

    def close_confirmed(self):
        # TODO Send to the current screen for cleanup?
        self.root.leave()
        self.stop()

    def hook_keyboard(self, window, key, *ignored_args):               
        # This keyboard control is just for my convenience, not on app.
        print "KEY PRESSED: %s" % key
        if key == 27:
            # Escape
            if BasePopup.my_active:
                # Cancel any popup
                BasePopup.clear()
            else:
                if self.root.current == "Settings":
                    self.return_screen()
                elif self.root.current == "Pente" and \
                     self.pente_screen.confirmation_in_progress:
                    self.pente_screen.cancel_confirmation()
                else:
                    self.prompt_quit()
            return True

        elif key == 113:
            # 'q'
            if not self.root.current in ["Setup", "AI"]:
                self.prompt_quit()
            return True

        elif key == 13:
            # Enter
            if ConfirmPopup.is_active():
                ConfirmPopup.confirm()
            elif self.root.current == "Pente":
                self.show_menu_screen()
            return True

        elif key == 32:
            # Space
            # Ignore spaces on other pages, could be entering names
            if self.root.current == "Pente":
                if self.game.finished():
                    self.show_games_screen()
                else:
                    # Game in progress, prompt
                    msg_str = "Leave this game?"
                    ConfirmPopup.create_and_open(message=msg_str,
                        action=self.show_games_screen,
                        size_hint=(.6, .2))
                return True

        elif key == 111:
            if self.root.current in ("Load", "Pente"):
                # or any other screen with text input
                self.show_settings_screen()
                return True

        elif key == 100: # 'd'
            # Debug
            ab_m.debug = not ab_m.debug
            aip_m.set_skip_openings_book(ab_m.debug)
            print "Debug set to %s" % ab_m.debug
            st() # Could help sometimes?
            return True

        elif key == 8: # 'delete'
            if self.root.current == "Games":
                self.games_screen.delete_game()
            return True

        else:
            if key == 115:
                # 's' for setup
                if self.root.current == "Pente":
                    # Go to setup page
                    # Probably not for production?
                    self.edit_game()
                    return True

        return False

    def add_screen(self, scr_cls, scr_name, **kwargs):
        scr = scr_cls(name=scr_name, **kwargs)
        scr.app = self
        scr.config = self.config
        scr.gm = self.games_mgr
        scr.ob = self.openings_book
        scr.pm = self.games_mgr.players_mgr
        self.root.add_widget(scr)

    def random_transition(self):
        # The other transition types trigger a crash
        trans = self.root.transition = SlideTransition()

        dirs = ['right','up','down','left']
        try:
            dirs.remove(self.last_choice)
        except: pass
        dc = random.choice(dirs)
        self.last_choice = dc
        trans.direction = dc

    def build(self):
        '''
        # This may look OK on an iPad? Not so good on laptop ;)
        if Window.height < Window.width:
            Window.rotation = 90
        '''
        root = ps_m.PScreenManager()
        self.root = root
        
        self.random_transition()

        self.game = None

        self.games_mgr = GamesMgr()
        self.openings_book = ob_m.OpeningsBook(self.games_mgr)

        screens = [(MenuScreen, "Menu"), (SettingsScreen, "Settings"),
                   (SetupScreen, "Setup"), (GamesScreen, "Games"),
                   (AIPlayerScreen, "AI"),
                   ]

        # Assign to self.config so all screens can get at it.
        self.config = ConfigParser()
        self.config.read('pentai.ini')

        self.audio = a_m.Audio(self.config)

        for scr_cls, scr_name in screens:
            self.add_screen(scr_cls, scr_name)

        self.menu_screen = root.get_screen("Menu")
        self.setup_screen = root.get_screen("Setup")
        self.settings_screen = root.get_screen("Settings")
        self.games_screen = root.get_screen("Games")
        self.pente_screen = None

        EventLoop.window.bind(on_keyboard=self.hook_keyboard)                  
        self.popup = None

        # Pass the config to the settings screen to use it for the
        # Kivy Settings editor.
        self.settings_screen.set_config(self.config)

        return root
    
    def set_confirmation_popups(self):
        p_m.ConfirmPopup.bypass = \
            not self.config.getint("PentAI", "confirm_popups")

    def on_pause(self):
        return True

if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '457')
    Config.set('graphics', 'height', '720')

    PentAIApp().run()

