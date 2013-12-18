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
        MyConfirmPopup.active.ok_confirm()

    def on_open(self):
        MyConfirmPopup.active = self 

    def cancel_confirm(self):
        MyConfirmPopup.active = None
        self.dismiss()

    def ok_confirm(self):
        MyConfirmPopup.active = None
        self.action()

class PenteApp(App):
    game_filename = StringProperty("")

    def show_load(self):
        self.root.current = "Load"

    def cancel_game_file(self):
        self.game_filename = ""
        self.root.current = "Setup"

    def load_game_file(self, path, filenames):
        f_n = filenames
        full_path = os.path.join(path, filenames[0])
        self.game_filename = full_path

        # TODO: Check file parsed etc.
        self.setup_screen.set_GUI_from_file(full_path)
        self.root.current = "Setup" # TODO production app should start game.

    def start_game(self, game, startup_size, filename=""):
        pente_screen = PenteScreen(startup_size, name='Game', filename=self.game_filename)
        self.root.add_widget(pente_screen)

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
        print "KEY PRESSED: %s" % key
        if key == 27:
            # (i.e. Escape)
            # do something to prevent close eg. Popup
            msg_str = "Are you sure you want to quit?"
            MyConfirmPopup.create_and_open(message=msg_str,
                        action=self.close_confirmed,
                        size_hint=(.6, .2))
            return True
        elif key == 13:
            # (i.e. Enter)
            MyConfirmPopup.confirm()
        return False

    def build(self):
        '''
        # This may look OK on an iPad? Not so good on laptop ;)
        if Window.height < Window.width:
            Window.rotation = 90
        '''
        root = ScreenManager()
        self.root = root

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

