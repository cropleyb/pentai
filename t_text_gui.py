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

    def setUpWithOverrides(self, size=5, player1=None, player2=None, rules_str="standard"):
        rules = Rules(size, rules_str)
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
        self.assertEquals(game_aux_string, "* Bruce (0p) vs. DeepThunk (0p)\n")

    def test_player_names_after_move(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce"),
                                player2=HumanPlayer("DeepThunk"))
        self.game.set_move_number(2)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "Bruce (0p) vs. * DeepThunk (0p)\n")

    def test_aux_after_moves_and_capture(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce"),
                                player2=HumanPlayer("DeepThunk"))
        self.game.set_move_number(6)
        self.game.set_captured(0, 2)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "Bruce (1p) vs. * DeepThunk (0p)\n")

    def test_aux_after_moves_and_capture_keryo(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce"),
                                player2=HumanPlayer("DeepThunk"),
                                rules_str="keryo")
        self.game.set_move_number(3)
        self.game.set_captured(0, 3)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "* Bruce (3) vs. DeepThunk (0)\n")

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
'* Fred (0p) vs. Wilma (0p)\n'
'Your move, Fred:\n')

    def test_move_action(self):
        action = self.gui.get_action_from_string("b3")
        self.assertEquals(action, MoveAction(2,3))

# TODO: captures? clocks?

if __name__ == "__main__":
    unittest.main()


