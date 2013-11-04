#!/usr/bin/env python

import unittest

from game import *
from rules import *
from text_gui import *

class TextGuiTest(unittest.TestCase):
    def test_place_one_stone(self):
        rules = Rules(5, "standard")
        game = Game(rules)
        gui = TextGui(game)
        gui.place_stone(4,2,white)
        empty_game_string = gui.to_string()

        #self.assertEquals(empty_game_string,
#"       \n"
#"       \n"

'''
- Place stone (pos, colour)
- Remove stone (pos)
- add captured stone
- remove captured stone (for undo/rewind)
- draw board / flush() (pass for Kivy)
  - show who is to move (though this isn't a method of the class)
- get a move
'''

if __name__ == "__main__":
    unittest.main()



