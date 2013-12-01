from kivy.app import App
from kivy.config import Config
from kivy.clock import *

from kivy.uix.screenmanager import *

from setup_screen import *
from pente_screen import *

class PenteApp(App):

    def start_game(self, game):
        pente_screen = PenteScreen(name='Game Screen')
        self.root.add_widget(pente_screen)

        # load the game screen
        pente_screen.set_game(game)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(pente_screen.set_up_grid, 1)

        self.root.current = "Game Screen"

    def build(self):
        root = ScreenManager()
        self.root = root
        s = SetupScreen(name="Setup Screen")
        s.app = self
        root.add_widget(s)

        return root

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '700')

    PenteApp().run()

