from kivy.app import App
from kivy.config import Config
from kivy.clock import *
from kivy.base import *
#from kivy.core.window import Window # Hmmmm... TODO?

from kivy.uix.screenmanager import *

from setup_screen import *
from options_screen import *
from pente_screen import *
from menu_screen import *
from games_mgr import *

from kivy.properties import ObjectProperty

import os # TODO: Remove?
import time

class LoadScreen(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class BasePopup(Popup):
    """ There should only be one active popup at a time. """

    my_active = None

    def __init__(self, *args, **kwargs):
        super(BasePopup, self).__init__(*args, **kwargs)

    @staticmethod
    def confirm():
        if BasePopup.my_active != None:
            BasePopup.my_active.ok_confirm()

    def ok_confirm(self):
        BasePopup.my_active = None
        self.dismiss()
        return True

    @staticmethod
    def clear():
        a = BasePopup.my_active
        BasePopup.my_active = None
        a.dismiss()

    def on_open(self):
        BasePopup.my_active = self 

class MessagePopup(BasePopup):
    """ Message Popup is for errors so far. Click anywhere to dismiss. """

    def __init__(self, *args, **kwargs):
        self.auto_dismiss = True
        self.going = False
        super(MessagePopup, self).__init__(*args, **kwargs)
    
    def on_touch_down(self, touch):
        self.going = True
        return True

    def on_touch_up(self, touch):
        if self.going:
            self.ok_confirm()
        self.going = not self.going
        return super(BasePopup, self).on_touch_up(touch)

class ConfirmPopup(BasePopup):
    """ ConfirmPopup is for True/False confirmation popup with a message """
    confirm_prompt = StringProperty("")

    def __init__(self, message, action, *args, **kwargs):
        self.auto_dismiss = False
        self.title = "" # I don't like the default :)
        self.confirm_prompt = message
        self.action = action
        super(ConfirmPopup, self).__init__(*args, **kwargs)

    @staticmethod
    def create_and_open(message, action, *args, **kwargs):
        if BasePopup.my_active == None:
            # TODO: Do we dismiss any existing popup?
            BasePopup.my_active = \
                ConfirmPopup(*args, message=message,
                        action=action, **kwargs)
            BasePopup.my_active.open()

    def ok_confirm(self):
        if super(ConfirmPopup, self).ok_confirm():
            self.action()

class PenteApp(App):
    game_filename = StringProperty("")

    def display_error(self, message):
        self.popup = MessagePopup(title='Error', content=Label(text=message, font_size='20sp'), \
                size_hint=(.8, .2))
        self.popup.open()
        print message

    def show_load(self, ignored=None):
        self.root.current = "Load"
        try:
            if self.game != None:
                self.game.set_interrupted()
                self.game = None
            game_screen = self.root.get_screen("Game")
            self.root.remove_widget(game_screen)
        except ScreenManagerException:
            pass

    def show_options(self):
        self.root.current = "Options"

    def show_game(self):
        self.root.current = "Game"

    def new_game_cb(self):
        self.game_filename = ""
        self.setup_screen.load_file(None)
        self.root.current = "Setup"

    def load_game_file_cb(self, path, filenames):
        f_n = filenames
        try:
            full_path = os.path.join(path, filenames[0])
        except IndexError:
            self.display_error("Please select a game first")
            return
        self.load_game_file(full_path)
    
    def load_game_file(self, full_path=None):
        if full_path != None:
            self.game_filename = full_path
        if self.game_filename == "":
            self.game_filename = self.game.autosave_filename
        # TODO: Check file parsed etc.
        self.setup_screen.load_file(self.game_filename)
        # TODO production app should start game here.
        self.root.current = "Setup"

    def start_game(self, game, startup_size):
        # TODO: Move this?
        root = self.root
        try:
            old_game_screen = root.get_screen("Game")
            if old_game_screen != None:
                root.remove_widget(old_game_screen)
        except ScreenManagerException:
            pass

        pente_screen = PenteScreen(startup_size, name='Game', filename=self.game_filename)
        pente_screen.app = self
        root.add_widget(pente_screen)
        self.game_screen = pente_screen
        self.game = game

        # TODO: Move stuff into PenteScreen __init__?

        # load the game screen
        pente_screen.set_game(game)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(pente_screen.setup_grid, 1)

        self.root.current = "Game"

    def close_confirmed(self):
        # TODO Send to the current screen?
        self.stop()

    def hook_keyboard(self, window, key, *ignored_args):               
        # This keyboard control is just for my convenience, not on app.
        print "KEY PRESSED: %s" % key
        if key in (27, 113):
            # (i.e. Escape or 'q')
            # do something to prevent close eg. Popup
            
            if BasePopup.my_active:
                BasePopup.clear()
            else:
                msg_str = "Are you sure you want to quit?"
                ConfirmPopup.create_and_open(message=msg_str,
                            action=self.close_confirmed,
                            size_hint=(.8, .2))
            return True
        elif key == 13:
            # Enter
            ConfirmPopup.confirm()
            return True
        elif key == 32:
            # Space
            # Ignore spaces on other pages, could be entering names
            if self.root.current == "Game":
                if self.game.finished():
                    self.show_load()
                else:
                    # Game in progress, prompt
                    msg_str = "Leave this game?"
                    ConfirmPopup.create_and_open(message=msg_str,
                        action=self.show_load,
                        size_hint=(.6, .2))
                return True
        elif key == 111:
            if self.root.current in ("Load", "Game"):
                # or any other screen with text input
                self.show_options()
                return True
        else:
            if self.root.current == "Game" and \
                    key == 115:
                # 's' for options TODO: o
                # Go to options page
                self.load_game_file()
                return True
        return False

    def build(self):
        '''
        # This may look OK on an iPad? Not so good on laptop ;)
        if Window.height < Window.width:
            Window.rotation = 90
        '''
        root = ScreenManager()
        self.root = root

        self.game = None
        player_db_filename = os.path.join("db", "players.pkl")
        game_manager_filename = os.path.join("db", "games.pkl")
        self.games_mgr = GamesMgr(player_db_filename, \
                game_manager_filename)

        screens = [(LoadScreen, "Load"), (OptionsScreen, "Options"), \
                   (MenuScreen, "Menu"), (SetupScreen, "Setup")]
        for scr_cls, scr_name in screens:
            scr = scr_cls(name=scr_name)
            scr.app = self
            scr.gm = self.games_mgr
            root.add_widget(scr)
        self.setup_screen = root.get_screen("Setup")
        self.game_screen = None

        # Confirm Quit
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)                  
        self.popup = None

        return root

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '457')
    Config.set('graphics', 'height', '720')
    #Config.set('graphics', 'width', '320')
    #Config.set('graphics', 'height', '504')


    PenteApp().run()

