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
from kivy.properties import StringProperty
from kivy.config import Config


class Pente(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)

class Piece(Scatter):
    source = StringProperty(None)


class PenteApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)
        pics = {}
        brd = None
        for filename in ("./images/board.png",):
            try:
                # load the image
                fs = filename[:].strip()
                picture = Pente(source=filename)
                brd = picture
                pics[fs] = picture

                # add to the main field
                root.add_widget(picture)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % fs)

        for filename in ("./images/black.png",):
            try:
                # load the image
                fs = filename[:].strip()
                black = Piece(source=filename)
                pics[fs] = black

                # add to the board
                brd.add_widget(black)
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

