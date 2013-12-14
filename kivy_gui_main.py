from kivy.app import App
from kivy.config import Config
from kivy.clock import *
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

    def build(self):
        '''
        # This may look OK on an iPad?
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

