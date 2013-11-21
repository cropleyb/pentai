from os.path import join, dirname
from kivy.app import App
from kivy.config import Config
from kivy.clock import *

from kivy_gui import *

class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)

        # load the image
        board = Board()

        # add to the main field
        root.add_widget(board)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(board.set_up_grid, 1)

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    # Set the screen to a square for now
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '600')
    PenteApp().run()

