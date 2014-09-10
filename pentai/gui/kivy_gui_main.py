from kivy.app import App
from kivy.properties import StringProperty
import os
import pentai.base.logger as log

# TODO: Delay these imports somehow, until after __init__() and build()
from kivy.clock import *
from kivy.base import *

import pentai.db.zodb_dict as z_m

import pentai.gui.config as cf_m
import pentai.gui.guide as gd_m
import pentai.gui.p_screen_manager as ps_m
import pentai.gui.my_button
from pentai.gui.popup import *

from pentai.db.games_mgr import *
import pentai.db.openings_book as ob_m

class PentAIApp(App):
    game_filename = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.debug = False
        super(PentAIApp, self).__init__(*args, **kwargs)
        self.defaults = None
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

                    # Copy DB to user_data_dir
                    shutil.copy(fn_ext, dest)
                    '''
                    # Delete existing DB in user_data_dir
                    del_path = os.path.join(dest, fn_ext)
                    try:
                        os.unlink(del_path)
                    except OSError:
                        pass
                    '''

    def display_message(self, message, title=None):
        from kivy.uix.label import Label
        if not title:
            title="Error"
        self.popup = MessagePopup(title=title,
                content=Label(text=message, font_size='20sp'),
                size_hint=(.9, .2),
                timeout_val=3)
        self.popup.open()
        log.info(message)

    def is_current_screen(self, screen):
        return self.root.current_screen == screen

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
        if self.root.current_screen == "Intro":
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
        self.game = None

    def show_new_game_screen(self):
        self.game_filename = ""
        self.setup_screen.create_game()
        self.root.push_current("Setup")

    def get_screen(self, screen_name):
        return self.root.get_screen(screen_name)

    def edit_game(self, game=None):
        if not game is None:
            self.game = game
        self.setup_screen.alter_game(self.game)
        self.root.push_current("Setup")

    def show_game_setup_help(self, ignored=None):
        self.root.push_current("GameSetupHelp")

    def show_demo(self):
        # This is to allow the demo to be shown from the game screen help.
        if self.game:
            self.saved_pente_game_key = self.game.key()
            if self.pente_screen:
                self.pente_screen.leave_game()
        else:
            self.saved_pente_game_key = None

        self.saved_guide_state = self.guide.is_enabled()
        self.guide.disable()

        # After the demo, we only want to revert the persistent operations
        # done during the demo. Anything done so far should be kept.
        z_m.sync()

        import demo as d_m
        d = d_m.Demo(self, self.setup_screen.size)
        # Intercept all touch events
        self.root.push_demo(d)

        d.start()

    def finish_demo(self):
        import audio as a_m
        a_m.instance.cut_demo()
        self.game = None
        self.pop_screen()
        z_m.abort()

        self.root.set_demo(None)
        if self.saved_pente_game_key:
            gid = self.saved_pente_game_key
            game = self.games_mgr.get_game(gid)
            self.saved_pente_game_key = None
            self.start_game(game)
        try:
            if self.saved_guide_state:
                self.guide.enable()
            self.guide.unhighlight("rules_demo_id")
            self.guide.on_enter(self.root.current)
        except AttributeError:
            pass

    def in_demo_mode(self):
        return self.root.in_demo_mode()

    def load_game_file_cb(self, path, filenames):
        f_n = filenames
        try:
            full_path = os.path.join(path, filenames[0])
        except IndexError:
            self.display_message("Please select a game first")
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

    def set_default_game(self):
        import pentai.db.create_default_players as cdp_m
        cdp_m.set_default_game(self.get_game_defaults())

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

    def start_game(self, game, swap_colours=False, demo=False):
        # TODO: Move this?
        root = self.root
        try:
            prev_game_screen = root.get_screen("Pente")
            if prev_game_screen != None:
                root.remove_widget(prev_game_screen)
        except ps_m.ScreenManagerException:
            pass

        screen_size = root.get_size()

        from pente_screen import PenteScreen
        self.add_screen_inc_globals(PenteScreen,
            "Pente", screen_size=screen_size,
            filename=self.game_filename)

        self.pente_screen = root.get_screen("Pente")
        self.game = game

        # load the game screen
        self.pente_screen.set_game(game, swap_colours=swap_colours)

        log.debug("Calling set_live %s from app.start_game" % (not demo))
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
                if self.root.current == "Settings" or "Help" in str(self.root.current):
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
            #if self.root.current in ("Load", "Human", "AI"):
            if self.root.current in ("Load"):
                # TODO: Check if keyboard is open first.
                '''
                import kivy.uix.vkeyboard as vk_m
                if not vk_m.docked:
                '''
                self.root.current_screen.delete()
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
        
        log.debug("Create Games Mgr")
        self.games_mgr = GamesMgr()
        log.debug("Create Openings Book")
        self.openings_book = ob_m.OpeningsBook()
        log.debug("Created Book")
        
        import pentai.db.create_default_players as cdp
        cdp.create_default_players(self.get_game_defaults())

        self.pack_and_start()

    def pack_and_start(self):
        log.info("About to pack_and_start DB")
        # Finished loading openings games. Pack the DB to reclaim space 
        z_m.pack()
        log.info("Done packing DB")
        Clock.schedule_once(self.create_screens, 0)

    def create_screens(self, ignored=None):
        root = self.root

        log.debug("Creating screens")

        screens = root.get_all_screens()

        log.debug("Adding screens to SM")
        for scr_cls, scr_name in screens:
            self.add_screen_inc_globals(scr_cls, scr_name)

        self.menu_screen = root.get_screen("Menu")
        self.setup_screen = root.get_screen("Setup")
        self.settings_screen = root.get_screen("Settings")
        self.games_screen = root.get_screen("Load")
        self.pente_screen = None

        gd_m.the_app = self

        self.set_guide()

        self.popup = None

        log.debug("Showing menu")
        self.show_menu_screen()

    def set_guide(self):
        try:
            self.guide = misc()["guide"]
        except KeyError:
            self.guide = misc()["guide"] = gd_m.Guide()
            self.guide.restart()

        self.root.guide = self.guide
        guide_setting = self.config.get("PentAI", "guide_setting")
        self.guide.set_state(guide_setting)
        if guide_setting == "Restart":
            guide_setting = "On"
            self.config.set("PentAI", "guide_setting", guide_setting)
        return guide_setting

    def set_confirmation_popups(self):
        import pentai.gui.popup as p_m
        p_m.ConfirmPopup.bypass = \
            not self.config.getint("PentAI", "confirm_popups")

    def on_pause(self):
        return True

