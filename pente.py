'''
Pictures demo
=============

This is a basic picture viewer, using the scatter widget.
'''

import kivy
import pdb
kivy.require('1.0.6')

from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.config import Config


class Pente(Widget):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)

    def on_touch_down(self, touch):
        # Logger.info('TOUCH DOWN!')
        #for filename in ("./images/black.png",):
        for filename in ("./images/white_transparent.png",):
            try:
                # load the image
                self.piece = Piece(source=filename)
                self.piece.pos = touch.pos
                self.add_widget(self.piece)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)

    def on_touch_up(self, touch):
        pass
        #Logger.info('TOUCH UP!')

    def on_touch_move(self, touch):
        #Logger.info('TOUCH MOVE!')
        self.piece.pos = touch.pos
        # TODO
        #if touch.x < self.width / 3:
            #self.player1.center_y = touch.y
        #if touch.x > self.width - self.width / 3:
            #self.player2.center_y = touch.y

class Piece(Scatter):
    source = StringProperty(None)


class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)
        for filename in ("./images/board.png",):
            try:
                # load the image
                fs = filename[:].strip()
                picture = Pente(source=filename)

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

