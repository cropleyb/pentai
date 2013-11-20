'''
Pictures demo
=============

This is a basic picture viewer, using the scatter widget.
'''

import kivy
kivy.require('1.0.6')

from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.config import Config
from kivy.graphics import *
from kivy.clock import *

class InfoPanel(Widget):
    source = StringProperty(None)

class PanelInfo(Widget):
    pass

'''
GridLayout:
    cols: 2
	# Left panel - info
	GridLayout:
		rows: 3

		# Player info
		GridLayout:
			rows: 3
			cols: 2
			Label:
				text: "00:00"
				# size_hint_y: 1
			Label:
				text: "00:00"
				# size_hint_y: 1
			Label
				text: "Player1"
				# size_hint_y: 1
			Label
				text: "Player2"
				# size_hint_y: 1
			# TODO: captured pieces
'''

class Pente(Widget):
    pass

BOARD_SIZE = 9
white_filename = "./images/white_transparent.png"
black_filename = "./images/black_transparent.png"

class Board(Widget):
    source = StringProperty(None)

    def set_up_grid(self, _dt):
        size_x = self.size[0]
        size_y = self.size[1]

        with self.canvas:
            # Black grid lines
            Color(0, 0, 0)
            grid_size_x = float(size_x) / (BOARD_SIZE + 1)
            grid_size_y = float(size_y) / (BOARD_SIZE + 1)
            # horizontal lines
            for y in range(1,BOARD_SIZE+1):
                Rectangle(pos=(grid_size_x-1, grid_size_y*y-1), \
                          size=(grid_size_x * (BOARD_SIZE-1), 3))
            # vertical lines
            for x in range(1,BOARD_SIZE+1):
                Rectangle(pos=(grid_size_x*x-1, grid_size_y-1), \
                          size=(3, grid_size_y * (BOARD_SIZE-1)))

    def snap_to_grid(self, pos):
        GRID = BOARD_SIZE + 1
        # print "%s, %s" % (pos, self.size)
        # (367.0, 193.0), [800, 600]
        # 367 / 800

        size_x = self.size[0]
        size_y = self.size[1]
        snapped_x = round(pos[0] / size_x * GRID) * size_x / GRID
        snapped_y = round(pos[1] / size_y * GRID) * size_y / GRID
        return snapped_x, snapped_y

    def on_touch_down(self, touch):
        for filename in (white_filename,):
            try:
                # load the image
                self.piece = Piece(source=filename)
                self.piece.pos = self.snap_to_grid(touch.pos)
                self.add_widget(self.piece)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)

    def on_touch_up(self, touch):
        pass

    def on_touch_move(self, touch):
        self.piece.pos = self.snap_to_grid(touch.pos)

class Piece(Scatter):
    source = StringProperty(None)


class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)

        try:
            # load the image
            board = Board()

            # add to the main field
            root.add_widget(board)

        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % fs)

        Clock.schedule_once(board.set_up_grid, 1)

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
    PenteApp().run()

