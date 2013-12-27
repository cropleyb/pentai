from kivy.app import App
from kivy.config import Config
from kivy.clock import *
from kivy.base import *
#from kivy.core.window import Window # Hmmmm... TODO?

from kivy.uix.screenmanager import *

from setup_screen import *
from settings_screen import *
from pente_screen import *
from menu_screen import *

from kivy.properties import ObjectProperty

import os # TODO: Remove?

class LoadScreen(Screen):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MyConfirmPopup(Popup):
    confirm_prompt = StringProperty("")

    # There should only be one active popup at a time.
    active = None

    def __init__(self, message, action, *args, **kwargs):
        self.title = "Confirm"
        self.confirm_prompt = message
        self.action = action
        super(MyConfirmPopup, self).__init__(*args, **kwargs)

    @staticmethod
    def create_and_open(message, action, *args, **kwargs):
        if MyConfirmPopup.active == None:
            # TODO: Do we dismiss any existing popup?
            MyConfirmPopup.active = \
                MyConfirmPopup(*args, message=message, action=action, **kwargs)
            MyConfirmPopup.active.open()

    @staticmethod
    def confirm():
        if MyConfirmPopup.active != None:
            MyConfirmPopup.active.ok_confirm()

    def on_open(self):
        MyConfirmPopup.active = self 

    @staticmethod
    def cancel_confirm():
        a = MyConfirmPopup.active
        MyConfirmPopup.active = None
        a.dismiss()

    def ok_confirm(self):
        MyConfirmPopup.active = None
        self.dismiss()
        self.action()

class PenteApp(App):
    game_filename = StringProperty("")

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

    def new_game_cb(self):
        self.game_filename = ""
        self.setup_screen.load_file(None)
        self.root.current = "Setup"

    def load_game_file_cb(self, path, filenames):
        f_n = filenames
        try:
            full_path = os.path.join(path, filenames[0])
        except IndexError:
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
        root.add_widget(pente_screen)
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

    def hook_keyboard(self, window, key, *largs):               
        # This keyboard control is just for my convenience, not on app.
        print "KEY PRESSED: %s" % key
        if key == 27:
            # (i.e. Escape)
            # do something to prevent close eg. Popup
            
            if MyConfirmPopup.active:
                MyConfirmPopup.cancel_confirm()
            else:
                msg_str = "Are you sure you want to quit?"
                MyConfirmPopup.create_and_open(message=msg_str,
                            action=self.close_confirmed,
                            size_hint=(.6, .2))
            return True
        elif key == 13:
            # Enter
            MyConfirmPopup.confirm()
        elif key == 32:
            # Space
            #if self.root.current != "Setup":
            # Ignore spaces on setup page, could be entering names
            if self.root.current != "Game" or self.game.finished():
                self.show_load()
            else:
                # Game in progress, prompt
                msg_str = "Quit this game?"
                MyConfirmPopup.create_and_open(message=msg_str,
                    action=self.show_load,
                    size_hint=(.6, .2))
        elif key == 115:
            # 's' for settings
            self.load_game_file()
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

        screens = [(LoadScreen, "Load"), (SettingsScreen, "Settings"), \
                   (MenuScreen, "Menu"), (SetupScreen, "Setup")]
        for scr_cls, scr_name in screens:
            scr = scr_cls(name=scr_name)
            scr.app = self
            root.add_widget(scr)
        self.setup_screen = root.get_screen("Setup")

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

