#!/usr/bin/env python

import unittest

from game import *
from rules import *
from text_gui import *
from player import *

class TextGuiTest(unittest.TestCase):

    def setUp(self):
        self.setUpWithOverrides(
                size=5,
                player1=HumanPlayer("Fred"),
                player2=HumanPlayer("Wilma"))

    def setUpWithOverrides(self, size=5, player1=None, player2=None):
        rules = Rules(size, "standard")
        self.game = Game(rules, player1, player2)
        self.gui = TextGui(self.game)

    def test_show_empty_board(self):
        empty_game_string = self.gui.board_to_string()
        self.assertEquals(empty_game_string,
"   abcde\n"
" 5      \n"
" 4      \n"
" 3      \n"
" 2      \n"
" 1      \n")

    def test_place_one_stone(self):
        self.gui.place_stone(4,2,black)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcde\n"
" 5      \n"
" 4      \n"
" 3      \n"
" 2    B \n"
" 1      \n")

    def test_place_and_remove_stone(self):
        self.gui.place_stone(4,2,black)
        self.gui.remove_stone(4,2)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcde\n"
" 5      \n"
" 4      \n"
" 3      \n"
" 2      \n"
" 1      \n")

    def test_place_one_stone_different_size(self):
        self.setUpWithOverrides(7)
        self.gui.place_stone(4,2,black)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcdefg\n"
" 7        \n"
" 6        \n"
" 5        \n"
" 4        \n"
" 3        \n"
" 2    B   \n"
" 1        \n")

    def test_place_and_remove_one_stone_different_size(self):
        self.setUpWithOverrides(7)
        self.gui.place_stone(4,2,black)
        self.gui.remove_stone(4,2)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcdefg\n"
" 7        \n"
" 6        \n"
" 5        \n"
" 4        \n"
" 3        \n"
" 2        \n"
" 1        \n")

    def test_big_empty_board(self):
        self.setUpWithOverrides(13)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcdefghjklmn\n"
"13              \n"
"12              \n"
"11              \n"
"10              \n"
" 9              \n"
" 8              \n"
" 7              \n"
" 6              \n"
" 5              \n"
" 4              \n"
" 3              \n"
" 2              \n"
" 1              \n")

    def test_place_two_stones(self):
        self.gui.place_stone(4,2,black)
        self.gui.place_stone(4,3,white)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   abcde\n"
" 5      \n"
" 4      \n"
" 3    W \n"
" 2    B \n"
" 1      \n")

    def test_player_names(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce"),
                                player2=HumanPlayer("DeepThunk"))
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "* Bruce vs. DeepThunk\n")

    def test_player_names_after_move(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce"),
                                player2=HumanPlayer("DeepThunk"))
        self.game.move_number += 1
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "Bruce vs. * DeepThunk\n")

    def test_player_move_prompt(self):
        p = self.game.get_player(0)
        promptStr = p.prompt_for_action(self.gui)
        self.assertEquals(promptStr,
'   abcde\n'
' 5      \n'
' 4      \n'
' 3      \n'
' 2      \n'
' 1      \n'
'* Fred vs. Wilma\n'
'Your move, Fred:\n')

# TODO: input, clocks?

if __name__ == "__main__":
    unittest.main()



