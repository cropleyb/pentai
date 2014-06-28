from kivy.app import App
from kivy.clock import *
from kivy.base import *

#from kivy.config import Config
#from kivy.config import ConfigParser
import pentai.gui.config as cf_m

from kivy.uix.screenmanager import * # TODO: Remove

import pentai.base.logger as log
import pentai.db.zodb_dict as z_m
import p_screen_manager as ps_m

from menu_screen import *
from ai_player_screen import *
from human_player_screen import *
from setup_screen import *
from settings_screen import *
from games_screen import *
import pente_screen
from popup import *
import my_button

from pentai.db.games_mgr import *
import pentai.db.openings_book as ob_m
import pentai.db.openings_builder as obl_m

from kivy.properties import ObjectProperty

import pentai.ai.alpha_beta as ab_m

import os
import time
import copy as c_m

import demo as d_m

class PentAIApp(App):
    game_filename = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.debug = False
        super(PentAIApp, self).__init__(*args, **kwargs)
        #if True:
        if not "db.fs" in os.listdir(self.user_data_dir):
            log.info("Copying db")
            import shutil
            dest = self.user_data_dir
            for fn in ["db.fs", "db.fs.index"]:
                shutil.copy(fn, dest)

    def display_error(self, message):
        self.popup = MessagePopup(title='Error', content=Label(text=message, font_size='20sp'), \
                size_hint=(.9, .2),
                timeout_val=4)
        self.popup.open()
        log.info(message)

    def return_screen(self, ignored=None):
        self.root.return_screen()

    def show_settings_screen(self):
        self.root.set_current("Settings")

    def show_pente_screen(self):
        self.root.set_current("Pente")

    def show_games_screen(self, ignored=None):
        self.root.set_current("Games")

    def show_ai_screen(self, ignored=None):
        self.root.set_current("AI")

    def show_human_screen(self, ignored=None):
        self.root.set_current("Human")

    def show_menu_screen(self, ignored=None):
        self.root.set_current("Menu")

    def show_new_game_screen(self):
        self.game_filename = ""
        self.setup_screen.create_game()
        self.root.set_current("Setup")

    def show_demo(self):
        d = d_m.Demo(self, self.setup_screen.size)

        # Intercept all touch events
        self.root.set_demo(d)

        d.start()

    def finish_demo(self):
        a_m.instance.cut_demo()
        z_m.abort()

        self.show_menu_screen()
        self.pente_screen = None
        self.root.set_demo(None)

    def in_demo_mode(self):
        return self.root.in_demo_mode()

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

    def start_game(self, game, screen_size, swap_colours=False, demo=False):
        # TODO: Move this?
        root = self.root
        try:
            prev_game_screen = root.get_screen("Pente")
            if prev_game_screen != None:
                root.remove_widget(prev_game_screen)
        except ScreenManagerException:
            pass

        self.add_screen(pente_screen.PenteScreen,
            'Pente', screen_size=screen_size,
            filename=self.game_filename)

        self.pente_screen = root.get_screen("Pente")
        self.game = game

        # load the game screen
        self.pente_screen.set_game(game, swap_colours=swap_colours)

        # TODO
        self.pente_screen.set_live(not demo)

        self.show_pente_screen()

    def prompt_quit(self):
        msg_str = "Are you sure you want to quit?"
        ConfirmPopup.create_and_open(message=msg_str,
                    action=self.close_confirmed,
                    size_hint=(.8, .2))

    def close_confirmed(self):
        # TODO Send to the current screen for cleanup?
        current_screen = self.root.current_screen
        if current_screen:
            current_screen.on_pre_leave()
            current_screen.on_leave()
        z_m.sync()
        self.stop()

    def hook_keyboard(self, window, key, *ignored_args):               
        # This keyboard control is just for my convenience, not on app.
        log.info("KEY PRESSED: %s" % key)
        typing_screens = ["Setup", "AI", "Human"]
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
            if not self.root.current in typing_screens:
                self.prompt_quit()
            return True

        elif key == 114:
            # 'r'
            if not self.root.current in typing_screens:
                pente_screen.reverse_colours()
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
            if self.in_demo_mode():
                self.finish_demo()
                return True
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
            if not self.root.current in typing_screens:
                ab_m.debug = not ab_m.debug
                self.debug = ab_m.debug

                import pentai.ai.ai_player as aip_m # hack for debugging
                log.info("Debug set to %s" % ab_m.debug)
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
        scr.config = self.config # TODO: only use singleton accessor
        scr.gm = self.games_mgr
        scr.ob = self.openings_book
        scr.pm = self.games_mgr.players_mgr
        self.root.add_widget(scr)

    def build(self):
        '''
        ini_file = "pentai.ini"
        ini_path = os.path.join(self.user_data_dir, ini_file)
        if not ini_file in os.listdir(self.user_data_dir):
            log.info("Copying ini")
            import shutil
            shutil.copy(ini_file, ini_path)

        # Assign to self.config so all screens can get at it.
        self.config = ConfigParser()
        self.config.read(ini_path)
        '''
        ini_file = "pentai.ini"
        self.config = cf_m.create_config_instance(ini_file, self.user_data_dir)

        root = ps_m.PScreenManager()
        root.show_intro_screen()
        self.root = root

        self.audio = a_m.Audio(self.config)
        self.audio.schedule_music()
        
        Clock.schedule_once(self.build_more, 0.1)

        return root

    def build_more(self, ignored):
        self.game = None

        self.openings_builder_timeout = False
        Clock.schedule_once(self.ob_timeout, 10)

        log.debug("Create Games Mgr")
        self.games_mgr = GamesMgr()
        log.debug("Create Openings Book")
        self.openings_book = ob_m.OpeningsBook()
        log.debug("Created Book")
        
        Clock.schedule_once(self.load_games, 0.01)

    def ob_timeout(self, ignored):
        log.debug("Intro Time is up")
        self.openings_builder_timeout = True

    def load_games(self, ignored):
        if not self.openings_builder_timeout:
            enough = obl_m.build(self.openings_book, self.user_data_dir, count=2)
            if enough:
                # Might as well stop waiting
                self.openings_builder_timeout = True
                log.debug("OK that's enough")

            # TODO: Max DB space
            # We'll add some more, but give Kivy some CPU too.
            Clock.schedule_once(self.load_games, 0.1)
        else:
            log.info("About to pack DB")
            # Finished loading openings games. Pack the DB to reclaim space 
            z_m.pack()
            log.info("Done packing DB")
            # Don't need this variable any more
            del self.openings_builder_timeout
            Clock.schedule_once(self.create_screens, 0)

    def create_screens(self, ignored):
        root = self.root

        log.debug("Creating screens")
        screens = [(MenuScreen, "Menu"), (SettingsScreen, "Settings"),
                   (SetupScreen, "Setup"), (GamesScreen, "Games"),
                   (AIPlayerScreen, "AI"), (HumanPlayerScreen, "Human"),
                   ]

        log.debug("Adding screens to SM")
        for scr_cls, scr_name in screens:
            self.add_screen(scr_cls, scr_name)

        self.menu_screen = root.get_screen("Menu")
        self.setup_screen = root.get_screen("Setup")
        self.settings_screen = root.get_screen("Settings")
        self.games_screen = root.get_screen("Games")
        self.pente_screen = None

        EventLoop.window.bind(on_keyboard=self.hook_keyboard)                  
        self.popup = None
        log.debug("Showing menu")

        self.show_menu_screen()

    def set_confirmation_popups(self):
        p_m.ConfirmPopup.bypass = \
            not self.config.getint("PentAI", "confirm_popups")

    def on_pause(self):
        return True

