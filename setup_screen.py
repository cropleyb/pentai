from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import *
from kivy.uix.screenmanager import Screen

import rules
import game
import human_player
import ai_player
from defines import *

def create_player(player_type_widget, player_name, max_depth):
    if player_type_widget.val == 'Computer':
        p = ai_player.AIPlayer(player_name, 9, 0)
        p.set_max_depth(max_depth)
    else:
        p = human_player.HumanPlayer(player_name)
    return p

class MyCheckBoxList(GridLayout):
    text = StringProperty("")
    group = StringProperty("")
    values = ListProperty([])
    active = StringProperty("")

    def on_checkbox_active(self, checkbox, value):
        if checkbox.active:
            self.val = checkbox.val

    def set_active(self, val):
        """ Set the active value from outside """
        old = self.widgets_by_val[str(self.val)]
        old.active = False

        w = self.widgets_by_val[str(val)]
        w.active = True
        self.val = str(val)

    def __init__(self, *args, **kwargs):
        super(MyCheckBoxList, self).__init__(*args, **kwargs)
        l = Label(text=self.text)
        self.add_widget(l)
        vals_gl = GridLayout(cols=2)
        self.add_widget(vals_gl)
        self.widgets_by_val = {}

        first = True
        for v in self.values:
            l = Label(text=v)
            vals_gl.add_widget(l)

            cb = CheckBox(group=self.group, active=first)
            cb.bind(active=self.on_checkbox_active)
            cb.val = v
            if first:
                self.on_checkbox_active(cb, None)
            vals_gl.add_widget(cb)
            self.widgets_by_val[v] = cb

            first = False

class SetupScreen(Screen):
    black_name = StringProperty("Black")
    white_name = StringProperty("White")
    black_type_widget = ObjectProperty(None)
    white_type_widget = ObjectProperty(None)
    rules_widget = ObjectProperty(None)
    board_size_widget = ObjectProperty(None)
    max_depth_widget = ObjectProperty(None)

    def __init__(self, filename=None, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)

        top_gl = GridLayout(cols=1)
        self.add_widget(top_gl)

        bs_r_gl = GridLayout(cols=2)
        top_gl.add_widget(bs_r_gl)
        self.board_size_widget = MyCheckBoxList(group="board_size", text="Board Size",
                values=["9", "13", "19"])
        bs_r_gl.add_widget(self.board_size_widget)

        self.rules_widget = MyCheckBoxList(group="rules", text="Rules",
				values=['standard', 'tournament', 'keryo',
                    'freestyle', 'five in a row', 'no captures'])
        bs_r_gl.add_widget(self.rules_widget)

        players_gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        top_gl.add_widget(players_gl)

        gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        players_gl.add_widget(gl)
        l = Label(text="Black\nplayer\nname")
        gl.add_widget(l)
        self.black_name_widget = TextInput(text=self.black_name)
        self.black_name_widget.bind(text=self.set_player_name)
        gl.add_widget(self.black_name_widget)
        self.black_type_widget = MyCheckBoxList(group="black_type", text="",
                values=('Human', 'Computer'))
        gl.add_widget(self.black_type_widget)

        gl = GridLayout(cols=2, size_hint=(1, None), height=120)
        players_gl.add_widget(gl)
        l = Label(text="White\nplayer\nname")
        gl.add_widget(l)
        t = TextInput(text=self.white_name)
        self.white_name_widget = TextInput(text=self.white_name)
        self.white_name_widget.bind(text=self.set_player_name)
        gl.add_widget(self.white_name_widget)
        self.white_type_widget = MyCheckBoxList(group="white_type", text="",
                values=('Human', 'Computer'))
        gl.add_widget(self.white_type_widget)

        self.max_depth_widget = MyCheckBoxList(group="max_depth", text="Max Search Depth",
                values=('1', '2', '3', '4', '5', '6', '7', '8'))
        top_gl.add_widget(self.max_depth_widget)

        b = Button(size_hint=(.1, .1), text='Start Game', on_press=self.start_game)
        top_gl.add_widget(b)

        if filename != None:
            self.set_GUI_from_file(filename)

    def start_game(self, unused=None):
        g = self.set_up_game_from_GUI()
        self.app.start_game(g, self.size)

    def set_up_game_from_GUI(self):
        bs = int(self.board_size_widget.val)
        rstr = self.rules_widget.val
        r = rules.Rules(bs, rstr)

        max_depth = int(self.max_depth_widget.val)
        player1 = create_player(self.black_type_widget, self.black_name, max_depth)
        player2 = create_player(self.white_type_widget, self.white_name, max_depth)

        g = game.Game(r, player1, player2)
        return g

    def set_player_name(self, widget, val):
        if widget == self.black_name_widget:
            self.black_name = val
        else:
            self.white_name = val

    def set_GUI_from_file(self, filename):
        f = open(filename)
        g = game.Game(None, None, None) # Hmmm. TODO
        g.configure_from_str(f.read())
        self.black_name_widget.text = g.get_player_name(BLACK)
        self.white_name_widget.text = g.get_player_name(WHITE)
        self.board_size_widget.set_active(g.rules.size)
        self.rules_widget.set_active(g.rules.type_str)
