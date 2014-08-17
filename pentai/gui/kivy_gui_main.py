from kivy.app import App
from kivy.properties import StringProperty
import os
import pentai.base.logger as log

# TODO: Delay these imports somehow, until after __init__() and build()
from kivy.clock import *
from kivy.base import *

import pentai.gui.config as cf_m

from kivy.uix.screenmanager import * # TODO: Remove

import pentai.db.zodb_dict as z_m
import p_screen_manager as ps_m

import my_button

from pentai.db.games_mgr import *
import pentai.db.openings_book as ob_m
import pentai.db.openings_builder as obl_m

from popup import *

class PentAIApp(App):
    game_filename = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.debug = False
        super(PentAIApp, self).__init__(*args, **kwargs)
        self.defaults = None
        self.building_openings = False
        self.menu_screen = None
        self.intro_help_screen = None

        #if True:
        if False:
        #if not "db.fs.most" in os.listdir(self.user_data_dir):
            log.info("Copying db")
            import shutil
            dest = self.user_data_dir
            for fn in ["db.fs.most", "db.fs.openings"]:
                for ext in ["", ".index"]:
                    fn_ext = "%s%s" % (fn, ext)
                    '''
                    # Copy DB to user_data_dir
                    shutil.copy(fn_ext, dest)
                    '''
                    # Delete existing DB in user_data_dir
                    del_path = os.path.join(dest, fn_ext)
                    try:
                        os.unlink(del_path)
                    except OSError:
                        pass

    def display_error(self, message):
        from kivy.uix.label import Label
        self.popup = MessagePopup(title='Error', content=Label(text=message, font_size='20sp'), \
                size_hint=(.9, .2),
                timeout_val=4)
        self.popup.open()
        log.info(message)

    def show_intro_screen(self):
        self.root.push_current("Intro")

    def show_intro_help(self, ignored=None):
        if self.intro_help_screen is None:
            self.intro_help_screen = \
                    self.add_screen(ps_m.IntroHelpScreen, 'IntroHelp')
        self.root.push_current("IntroHelp")

    def pop_screen(self, ignored=None):
        ok = self.root.pop_screen()
        if not ok:
            self.create_screens()
        if self.root.current_screen == "Intro" and not self.building_openings:
            ok = self.root.pop_screen()

    def show_settings_screen(self):
        self.root.push_current("Settings")

    def show_settings_help(self, ignored=None):
        self.root.push_current("SettingsHelp")

    def show_pente_screen(self):
        self.root.set_current("Pente")

    def show_pente_help(self, ignored=None):
        self.root.push_current("PenteHelp")

    def show_games_screen(self, ignored=None, finished=False):
        self.games_screen.set_show_finished(finished)
        self.root.set_current("Load")

    def show_load_help(self, ignored=None):
        self.root.push_current("LoadHelp")

    def show_ai_screen(self, ignored=None):
        self.root.set_current("AI")

    def show_ai_help(self, ignored=None):
        self.root.push_current("AIHelp")

    def show_human_screen(self, ignored=None):
        self.root.set_current("Human")

    def show_human_help(self, ignored=None):
        self.root.push_current("HumanHelp")

    def show_menu_screen(self, ignored=None):
        self.root.set_current("Menu")
        self.root.clear_hist()

    def show_new_game_screen(self):
        self.game_filename = ""
        self.setup_screen.create_game()
        self.root.push_current("Setup")

    def edit_game(self, game=None):
        if not game is None:
            self.game = game
        self.setup_screen.alter_game(self.game)
        self.root.push_current("Setup")

    def show_game_setup_help(self, ignored=None):
        self.root.push_current("GameSetupHelp")

    def show_demo(self):
        import demo as d_m
        self.saved_pente_screen = self.pente_screen
        d = d_m.Demo(self, self.setup_screen.size)
        # Intercept all touch events
        self.root.push_demo(d)

        d.start()

    def finish_demo(self):
        import audio as a_m
        a_m.instance.cut_demo()
        z_m.abort()

        #self.show_menu_screen()
        self.pop_screen()
        self.pente_screen = self.saved_pente_screen
        #self.pente_screen = None
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

    def get_game_defaults(self):
        import pentai.gui.game_defaults as gd_m
        if not self.defaults:
            try:
                self.defaults = misc()["game_defaults"]
            except KeyError:
                self.defaults = misc()["game_defaults"] = gd_m.GameDefaults()
        return self.defaults

    def load_game_file(self, full_path=None):
        if full_path != None:
            self.game_filename = full_path
        if self.game_filename == "":
            self.game_filename = self.game.autosave_filename
        # TODO: Check file parsed etc.
        self.setup_screen.load_file(self.game_filename)
        # TODO production app should start game here.
        self.root.current = "Setup"

    def openings_book_is_finished(self):
        return obl_m.is_finished()

    def build_all_openings(self):
        self.building_openings = True
        self.show_intro_screen()
        Clock.schedule_once(self.build_all_openings_inner, 0.1)

    def build_all_openings_inner(self, *ignored):
        enough = obl_m.build(self.openings_book, self.user_data_dir, count=2)
        if enough:
            # UI bypass will skip the pack() call
            z_m.pack()
            self.building_openings = False
            self.pop_screen()
        if self.building_openings:
            Clock.schedule_once(self.build_all_openings_inner, 0.1)

    def start_game(self, game, screen_size, swap_colours=False, demo=False):
        # TODO: Move this?
        root = self.root
        try:
            prev_game_screen = root.get_screen("Pente")
            if prev_game_screen != None:
                root.remove_widget(prev_game_screen)
        except ScreenManagerException:
            pass

        from pente_screen import PenteScreen
        self.add_screen_inc_globals(PenteScreen,
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
            if self.building_openings:
                self.interrupt_openings_building()
            elif BasePopup.my_active:
                # Cancel any popup
                BasePopup.clear()
            else:
                if self.root.current == "Settings":
                    self.pop_screen()
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
                import pentai.ai.alpha_beta as ab_m
                ab_m.debug = not ab_m.debug
                self.debug = ab_m.debug

                import pentai.ai.ai_player as aip_m # hack for debugging
                log.info("Debug set to %s" % ab_m.debug)
                st() # Could help sometimes?
                return True

        elif key == 8: # 'delete'
            if self.root.current == "Load":
                self.games_screen.delete_game()
            return True

        elif key == 115:
                # 's' for setup
                if self.root.current == "Pente":
                    # Go to setup page
                    # Probably not for production?
                    self.edit_game()
                    return True

        elif key == 97: # 'a' for Assess
            if self.root.current == "Pente":
                self.pente_screen.assess()
            return True

        return False

    def add_screen(self, scr_cls, scr_name, **kwargs):
        scr = scr_cls(name=scr_name, **kwargs)
        scr.app = self
        scr.config = self.config # TODO: only use singleton accessor
        self.root.add_widget(scr)
        return scr

    def add_screen_inc_globals(self, scr_cls, scr_name, **kwargs):
        scr = self.add_screen(scr_cls, scr_name, **kwargs)
        scr.gm = self.games_mgr
        scr.ob = self.openings_book
        scr.pm = self.games_mgr.players_mgr

    def build(self):
        log.debug("app build 1")
        ini_file = "pentai.ini"
        if False:
        #if True:
            # Keep this for developing new config items
            log.info("Copying init")
            import shutil
            dest = self.user_data_dir
            shutil.copy(ini_file, dest)
        log.debug("app build 2")
        self.config = cf_m.create_config_instance(ini_file, self.user_data_dir)

        root = ps_m.PScreenManager()
        self.root = root
        self.add_screen(ps_m.IntroScreen, 'Intro')
        log.debug("app build 3")
        self.show_intro_screen()
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)                  

        import audio as a_m
        self.audio = a_m.Audio(self.config)
        log.debug("app build 4")
        self.audio.schedule_music()
        log.debug("app build 5")
        
        Clock.schedule_once(self.build_more, 0.1)
        
        return root

    def build_more(self, ignored):
        self.game = None
        
        #self.building_openings = True
        Clock.schedule_once(self.interrupt_openings_building, 10)

        log.debug("Create Games Mgr")
        self.games_mgr = GamesMgr()
        log.debug("Create Openings Book")
        self.openings_book = ob_m.OpeningsBook()
        log.debug("Created Book")
        
        import pentai.db.create_default_players as cdp
        cdp.create_default_players()

        obb = self.config.get("PentAI", "openings_book_building")
        if obb == "Part On Startup":
            self.building_openings = True
            Clock.schedule_once(self.load_games, 0.01)
        else:
            self.pack_and_start()

    def interrupt_openings_building(self, ignored=None):
        log.debug("Stop building openings book")
        self.building_openings = False

    def load_games(self, ignored):
        if not self.building_openings:
            self.pack_and_start()
        else:
            enough = obl_m.build(self.openings_book, self.user_data_dir, count=2)
            if enough:
                # Might as well stop waiting
                self.building_openings = False
                log.debug("OK that's enough")

            # TODO: Max DB space
            # We'll add some more, but give Kivy some CPU too.
            Clock.schedule_once(self.load_games, 0.1)

    def pack_and_start(self):
        log.info("About to pack_and_start DB")
        # Finished loading openings games. Pack the DB to reclaim space 
        z_m.pack()
        log.info("Done packing DB")
        Clock.schedule_once(self.create_screens, 0)

    def create_screens(self, ignored=None):
        if not self.menu_screen is None:
            self.show_menu_screen()

        root = self.root

        log.debug("Creating screens")

        self.building_openings = False

        screens = root.get_all_screens()

        log.debug("Adding screens to SM")
        for scr_cls, scr_name in screens:
            self.add_screen_inc_globals(scr_cls, scr_name)

        self.menu_screen = root.get_screen("Menu")
        self.setup_screen = root.get_screen("Setup")
        self.settings_screen = root.get_screen("Settings")
        self.games_screen = root.get_screen("Load")
        self.pente_screen = None

        self.popup = None

        log.debug("Showing menu")
        self.show_menu_screen()

    def set_confirmation_popups(self):
        import pentai.gui.popup as p_m
        p_m.ConfirmPopup.bypass = \
            not self.config.getint("PentAI", "confirm_popups")

    def on_pause(self):
        return True

