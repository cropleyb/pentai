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

black_filename = "./images/black_transparent.png"
white_filename = "./images/white_transparent.png"
x_filename = "./images/X_transparent.png"

class Board(Widget):
    source = StringProperty(None)

    def __init__(self, *args, **kwargs):
        self.marker = None
        self.move_number = 0
        self.BOARD_SIZE = 9

        # The Grid on the screen allows extra space at the edges
        self.GRID_SIZE = self.BOARD_SIZE + 1

        self.stones_by_board_pos = {}
        super(Board, self).__init__(*args, **kwargs)

    def set_up_grid(self, _dt):
        size_x = self.size[0]
        size_y = self.size[1]

        with self.canvas:
            # Black grid lines
            Color(0, 0, 0)
            grid_size_x = float(size_x) / (self.GRID_SIZE)
            grid_size_y = float(size_y) / (self.GRID_SIZE)
            # horizontal lines
            for y in range(1,self.GRID_SIZE):
                Rectangle(pos=(grid_size_x-1, grid_size_y*y-1), \
                          size=(grid_size_x * (self.GRID_SIZE-2), 3))
            # vertical lines
            for x in range(1,self.GRID_SIZE):
                Rectangle(pos=(grid_size_x*x-1, grid_size_y-1), \
                          size=(3, grid_size_y * (self.GRID_SIZE-2)))

    def snap_to_grid(self, screen_pos):
        return self.board_to_screen(self.screen_to_board(screen_pos))

    def screen_to_board(self, screen_pos):
        """ Convert a screen position (in pixels) to a board coordinate pair,
            dependant on the size of the board """
        size_x, size_y = self.size
        GS = self.GRID_SIZE
        board_x = round(GS * screen_pos[0] / size_x) - 1
        board_y = round(GS * screen_pos[1] / size_y) - 1
        return board_x, board_y

    def board_to_screen(self, board_pos):
        """ Convert a board coordinate pair to a screen position (in pixels),
            dependant on the size of the board """
        size_x, size_y = self.size
        GS = self.GRID_SIZE
        screen_x = ((board_pos[0] + 1) / GS) * size_x
        screen_y = ((board_pos[1] + 1) / GS) * size_y
        return screen_x, screen_y

    def on_touch_down(self, touch):
        # Place a marker at the (snapped) cursor position.
        if self.marker == None:
            try:
                # load the image
                # TODO: Separate class?
                self.marker = Piece(source=x_filename)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % x_filename)
        self.marker.pos = self.snap_to_grid(touch.pos)
        self.add_widget(self.marker)

    def on_touch_up(self, touch):
        # If there is an active marker:
        # Replace the marker to a piece of the appropriate colour
        # TODO: make the move with the appropriate board position
        if self.marker != None:
            self.remove_widget(self.marker)
            # Quick hack to get both coloured stones on the board
            board_pos = self.screen_to_board(touch.pos)

            if self.stones_by_board_pos.has_key(board_pos):
                # There is a piece there already, remove it.
                current_piece = self.stones_by_board_pos[board_pos]
                self.remove_widget(current_piece)
            else:
                # Nothing there yet, place a stone
                to_move = self.move_number % 2
                filename = [white_filename, black_filename][to_move]
                self.move_number += 1
                try:
                    # load the image
                    new_piece = Piece(source=filename)
                    self.stones_by_board_pos[board_pos] = new_piece
                    new_piece.pos = self.board_to_screen(board_pos)
                    #self.new_piece.pos = self.snap_to_grid(touch.pos)
                    self.add_widget(new_piece)
                except Exception, e:
                    Logger.exception('Board: Unable to load <%s>' % filename)

    def on_touch_move(self, touch):
        # Move the marker position
        if self.marker != None:
            self.marker.pos = self.snap_to_grid(touch.pos)

class Piece(Scatter):
    source = StringProperty(None)


class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)

        #try:
        # load the image
        board = Board()

        # add to the main field
        root.add_widget(board)

        #except Exception, e:
            #Logger.exception('Board: Unable to load <%s>' % fs)

        Clock.schedule_once(board.set_up_grid, 1)

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '600')
    PenteApp().run()

