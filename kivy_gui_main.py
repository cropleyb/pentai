from os.path import join, dirname
from kivy.app import App
from kivy.config import Config
from kivy.clock import *

from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.screenmanager import *

from kivy.properties import ObjectProperty, BooleanProperty

import rules
import game
import human_player
import ai_player


import argparse

from pente_screen import *

global args
args = None

'''
class LabelledCheckbox(Widget):
    value = ObjectProperty(None)
	callback: None
    group = StringProperty("")
	active = BooleanProperty(False)
'''

class MyCheckBoxList(Widget):
    text = StringProperty("")
    group = StringProperty("")
    values = ListProperty([])
    active = StringProperty("")

    # def on_checkbox_active(checkbox, value):
    def on_checkbox_active(self, checkbox, value):
        self.val = checkbox.val

    def __init__(self, *args, **kwargs):
        super(MyCheckBoxList, self).__init__(*args, **kwargs)
        #gl = GridLayout(cols=2)
        gl = GridLayout(cols=2, size_hint=(1, 1))
        self.add_widget(gl)
        l = Label(text=self.text)
        gl.add_widget(l)
        vals_gl = GridLayout(cols=2, size_hint=(1, 1))
        gl.add_widget(vals_gl)

        first = True
        for v in self.values:
            '''
            cb = LabelledCheckbox(value=v, callback=self.set_active,
                    group=self.group, active=first)
            '''
            l = Label(text=v)
            vals_gl.add_widget(l)

            cb = CheckBox(group=self.group, active=first)
            cb.bind(active=self.on_checkbox_active)
            cb.val = v
            if first:
                self.on_checkbox_active(cb, None)
            vals_gl.add_widget(cb)
            first = False


class SetupScreen(Screen):
    black_name = StringProperty("Black")
    white_name = StringProperty("White")

    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        top_gl = GridLayout(cols=1, size_hint=(1, 1))
        self.add_widget(top_gl)

        bs_r_gl = GridLayout(cols=2, height=500, size_hint=(1, 1))
        top_gl.add_widget(bs_r_gl)
        self.board_size_widget = MyCheckBoxList(group="board_size", text="Board Size",
                values=["9", "13", "19"])
        bs_r_gl.add_widget(self.board_size_widget)

        self.rules_widget = MyCheckBoxList(group="rules", text="Rules",
				values=['standard', 'tournament', 'keryo', 'freestyle', 'five', 'no'])
        bs_r_gl.add_widget(self.rules_widget)

        players_gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        top_gl.add_widget(players_gl)

        gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        players_gl.add_widget(gl)
        l = Label(text="Black player name")
        gl.add_widget(l)
        t = TextInput(text=self.black_name)
        gl.add_widget(t)
        self.black_type_widget = MyCheckBoxList(group="black_type", text="", values=('Human', 'Computer'))
        gl.add_widget(self.black_type_widget)

        gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        players_gl.add_widget(gl)
        l = Label(text="White player name")
        gl.add_widget(l)
        t = TextInput(text=self.white_name)
        gl.add_widget(t)
        self.white_type_widget = MyCheckBoxList(group="white_type", text="", values=('Human', 'Computer'))
        gl.add_widget(self.white_type_widget)

        b = Button(size_hint=(.1, .1), text='Start Game', on_press=self.start_game)
        top_gl.add_widget(b)

    def start_game(self, cb):
        g = self.set_up_game()
        app.start_game(g)

    def set_up_game(self):
        r = rules.Rules(int(self.board_size_widget.val), self.rules_widget.val)

        player1_type = human_player.HumanPlayer
        if self.black_type_widget.val == 'Computer':
            player1_type = human_player.AIPlayer
        player1 = player1_type(self.black_name)

        player2_type = human_player.HumanPlayer
        if self.white_type_widget.val == 'Computer':
            player2_type = human_player.AIPlayer
        player2 = player2_type(self.white_name)

        g = game.Game(r, player1, player2)
        return g
    pass

class PenteApp(App):

    def start_game(self, game):
        pente_screen = PenteScreen(name='Game Screen')
        self.root.add_widget(pente_screen)

        # get any files into images directory
        curdir = dirname(__file__)

        # load the game screen
        pente_screen.set_game(game)

        # TODO: It would be nice if the board did not display until the grid was
        # correctly positioned
        Clock.schedule_once(pente_screen.set_up_grid, 1)

        self.root.current = "Game Screen"

    def build(self):
        root = ScreenManager()
        self.root = root
        root.add_widget(SetupScreen(name="Setup Screen"))

        global app
        app = self

        '''
        if True:

            g = self.set_up_game()

            # load the game screen
            pente_screen.set_game(g)

            # TODO: It would be nice if the board did not display until the grid was
            # correctly positioned
            Clock.schedule_once(pente_screen.set_up_grid, 1)
        '''

        return root

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

