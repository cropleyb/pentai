#!/usr/bin/env python

import unittest

from game import *
from rules import *
from text_gui import *

class TextGuiTest(unittest.TestCase):

    def setUp(self):
        self.setUpWithSize(5)

    def setUpWithSize(self, size):
        rules = Rules(size, "standard")
        game = Game(rules)
        self.gui = TextGui(game)

    def test_show_empty_board(self):
        empty_game_string = self.gui.board_to_string()
        self.assertEquals(empty_game_string,
" abcde\n"
"5     \n"
"4     \n"
"3     \n"
"2     \n"
"1     \n")

    def test_place_one_stone(self):
        self.gui.place_stone(4,2,black)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
" abcde\n"
"5     \n"
"4     \n"
"3     \n"
"2   B \n"
"1     \n")

    def test_place_and_remove_stone(self):
        self.gui.place_stone(4,2,black)
        self.gui.remove_stone(4,2)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
" abcde\n"
"5     \n"
"4     \n"
"3     \n"
"2     \n"
"1     \n")

    def test_place_one_stone_different_size(self):
        self.setUpWithSize(7)
        self.gui.place_stone(4,2,black)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
" abcdefg\n"
"7       \n"
"6       \n"
"5       \n"
"4       \n"
"3       \n"
"2   B   \n"
"1       \n")

    def test_place_and_remove_one_stone_different_size(self):
        self.setUpWithSize(7)
        self.gui.place_stone(4,2,black)
        self.gui.remove_stone(4,2)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
" abcdefg\n"
"7       \n"
"6       \n"
"5       \n"
"4       \n"
"3       \n"
"2       \n"
"1       \n")

# TODO: input, player?

if __name__ == "__main__":
    unittest.main()



