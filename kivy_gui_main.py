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

BOARD_SIZE = 13

class Board(Widget):
    source = StringProperty(None)

    def snap_to_grid(self, pos):
        BS = BOARD_SIZE + 1
        print "%s, %s" % (pos, self.size)
        # (367.0, 193.0), [800, 600]
        # 367 / 800

        snapped_x = round(pos[0] / self.size[0] * BS) * self.size[0] / BS
        snapped_y = round(pos[1] / self.size[1] * BS) * self.size[1] / BS
        return snapped_x, snapped_y

    def on_touch_down(self, touch):
        for filename in ("./images/white_transparent.png",):
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
            filename = "./images/board.png"
            fs = filename[:].strip()
            picture = Board(source=filename)

            # add to the main field
            root.add_widget(picture)
        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % fs)

    def on_pause(self):
        return True


if __name__ == '__main__':
    Config.set('kivy', 'log_level', 'info')
    Config.set('kivy', 'log_enable', 1)
    Config.set('kivy', 'log_dir', 'logs')
    Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
    PenteApp().run()

