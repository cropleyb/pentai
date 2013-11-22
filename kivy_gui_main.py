from os.path import join, dirname
from kivy.app import App
from kivy.config import Config
from kivy.clock import *

import rules
import game
import human_player
import ai_player

from kivy_gui import *

class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)

        self.set_up_game()

        # load the board image
        board_widget = BoardWidget()

        board_widget.set_game(self.game)

        # add to the main field
        root.add_widget(board_widget)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(board_widget.set_up_grid, 1)

    def set_up_game(self):
        r = rules.Rules(9, "standard")
        player1 = human_player.HumanPlayer("Bruce", BLACK)
        '''
        player2 = human_player.HumanPlayer("B2", WHITE)
        '''
        player2 = ai_player.AIPlayer(1, "Deep Thunk", WHITE)
        self.game = game.Game(r, player1, player2)
        player2.attach_to_game(self.game)

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

