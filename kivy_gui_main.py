from os.path import join, dirname
from kivy.app import App
from kivy.config import Config
from kivy.clock import *

from kivy.uix.screenmanager import Screen

import rules
import game
import human_player
import ai_player

import argparse

from kivy_gui import *

global args
args = None

class SetupScreen(Screen):
    pass

class PenteApp(App):

    def build(self):

        # get any files into images directory
        curdir = dirname(__file__)

        g = self.set_up_game()

        # load the game screen
        game_widget = PenteScreen()

        game_widget.set_game(g)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(game_widget.set_up_grid, 1)

        # Returning the widget assigns the "root" variable
        return game_widget

    def set_up_game(self):
        r = rules.Rules(args.board_size, args.rules)

        player1_type = human_player.HumanPlayer
        if args.b_type == 'Computer':
            player1_type = human_player.AIPlayer
        player1 = player1_type(args.black)

        player2_type = human_player.HumanPlayer
        if args.b_type == 'Computer':
            player2_type = human_player.AIPlayer
        player2 = player2_type(args.white)

        g = game.Game(r, player1, player2)
        return g

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')

    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '700')

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('board_size', metavar='s', type=int, nargs='?',
        default=13, help='How wide is the board')
    parser.add_argument('rules', type=str, nargs='?',
        default='standard', help='Which rule set do you want to play', choices=(
        'standard', 'tournament', 'keryo', 'freestyle', 'five', 'no'))
    parser.add_argument('black', metavar='B', type=str, nargs='?',
        default='Black Player', help='Black Player\'s Name')
    parser.add_argument('white', metavar='W', type=str, nargs='?',
        default='White Player', help='White Player\'s Name')
    parser.add_argument('b_type', metavar='b', type=str, nargs='?', choices=('H','C'),
        default='H', help='Black - (H)uman or (C)omputer')
    parser.add_argument('w_type', metavar='w', type=str, nargs='?', choices=('H','C'),
        default='H', help='White - (H)uman or (C)omputer')

    args = parser.parse_args()

    PenteApp().run()

