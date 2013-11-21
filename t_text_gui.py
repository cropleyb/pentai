#!/usr/bin/env python

import unittest

from game import *
from rules import *
from text_gui import *
from pente_exceptions import *
from human_player import *

import pdb

class TextGuiTest(unittest.TestCase):

    def setUp(self):
        self.setUpWithOverrides(
                size=5,
                player1=HumanPlayer("Fred", BLACK),
                player2=HumanPlayer("Wilma", WHITE))

    def setUpWithOverrides(self, size=5, player1=None, player2=None, rules_str="standard"):
        rules = Rules(size, rules_str)
        self.game = Game(rules, player1, player2)
        self.gui = TextGui(self.game)

    def test_show_empty_board(self):
        empty_game_string = self.gui.board_to_string()
        self.assertEquals(empty_game_string,
"   a b c d e\n"
" 5          \n"
" 4          \n"
" 3          \n"
" 2          \n"
" 1          \n"
"   a b c d e\n")

    def test_place_one_stone(self):
        self.gui.after_set_occ((3,1), BLACK)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e\n"
" 5          \n"
" 4          \n"
" 3          \n"
" 2       B  \n"
" 1          \n"
"   a b c d e\n")

    def test_place_and_remove_stone(self):
        self.gui.after_set_occ((4,2),BLACK)
        self.gui.after_set_occ((4,2),EMPTY)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e\n"
" 5          \n"
" 4          \n"
" 3          \n"
" 2          \n"
" 1          \n"
"   a b c d e\n")

    def test_place_one_stone_different_size(self):
        self.setUpWithOverrides(7)
        self.gui.after_set_occ((3,1),BLACK)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e f g\n"
" 7              \n"
" 6              \n"
" 5              \n"
" 4              \n"
" 3              \n"
" 2       B      \n"
" 1              \n"
"   a b c d e f g\n")

    def test_place_and_remove_one_stone_different_size(self):
        self.setUpWithOverrides(7)
        self.gui.after_set_occ((4,2),BLACK)
        self.gui.after_set_occ((4,2),EMPTY)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e f g\n"
" 7              \n"
" 6              \n"
" 5              \n"
" 4              \n"
" 3              \n"
" 2              \n"
" 1              \n"
"   a b c d e f g\n")

    def test_big_empty_board(self):
        self.setUpWithOverrides(13)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e f g h j k l m n\n"
"13                          \n"
"12                          \n"
"11                          \n"
"10                          \n"
" 9                          \n"
" 8                          \n"
" 7                          \n"
" 6                          \n"
" 5                          \n"
" 4                          \n"
" 3                          \n"
" 2                          \n"
" 1                          \n"
"   a b c d e f g h j k l m n\n")

    def test_place_two_stones(self):
        self.gui.after_set_occ((4,2),BLACK)
        self.gui.after_set_occ((4,3),WHITE)
        game_string = self.gui.board_to_string()
        self.assertEquals(game_string,
"   a b c d e\n"
" 5          \n"
" 4         W\n"
" 3         B\n"
" 2          \n"
" 1          \n"
"   a b c d e\n")

    def test_player_names(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce", BLACK),
                                player2=HumanPlayer("DeepThunk", WHITE))
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "* Bruce (0p) vs. DeepThunk (0p)\n")

    def test_player_names_after_move(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce", BLACK),
                                player2=HumanPlayer("DeepThunk", WHITE))
        self.game.set_move_number(2)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "Bruce (0p) vs. * DeepThunk (0p)\n")

    def test_aux_after_moves_and_capture(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce", BLACK),
                                player2=HumanPlayer("DeepThunk", WHITE))
        self.game.set_move_number(6)
        self.game.set_captured(0, 2)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "Bruce (1p) vs. * DeepThunk (0p)\n")

    def test_aux_after_moves_and_capture_keryo(self):
        self.setUpWithOverrides(player1=HumanPlayer("Bruce", BLACK),
                                player2=HumanPlayer("DeepThunk", WHITE),
                                rules_str="keryo")
        self.game.set_move_number(3)
        self.game.set_captured(0, 3)
        game_aux_string = self.gui.aux_to_string()
        self.assertEquals(game_aux_string, "* Bruce (3) vs. DeepThunk (0)\n")

    def test_player_move_prompt(self):
        p = self.game.get_player(0)
        promptStr = p.prompt_for_action(self.game, self.gui)
        self.assertEquals(promptStr,
'   a b c d e\n'
' 5          \n'
' 4          \n'
' 3          \n'
' 2          \n'
' 1          \n'
'   a b c d e\n'
'* Fred (0p) vs. Wilma (0p)\n'
'Your move, Fred:\n')

    def test_move_action(self):
        action = self.gui.get_action_from_string("b3")
        self.assertEquals(action, MoveAction((1,2)))

    def test_move_action_illegal_char(self):
        try:
            action = self.gui.get_action_from_string("@1")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return
        self.fail()

    def test_move_action_L_front(self):
        action = self.gui.get_action_from_string("a1")
        self.assertEquals(action, MoveAction((0,0)))

    def test_move_action_R_back(self):
        action = self.gui.get_action_from_string("e5")
        self.assertEquals(action, MoveAction((4,4)))

    def test_off_board_move_R(self):
        try:
            action = self.gui.get_action_from_string("f5")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return
        self.fail()

    def test_off_board_move_top(self):
        try:
            action = self.gui.get_action_from_string("e6")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return
        self.fail()

    def test_off_board_move_bottom(self):
        try:
            action = self.gui.get_action_from_string("e0")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return

    def test_off_board_move_left(self):
        try:
            action = self.gui.get_action_from_string("_3")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return
        self.fail()

    def test_off_board_move_right(self):
        try:
            action = self.gui.get_action_from_string("f3")
        except IllegalMoveException, e:
            self.assertEquals(e.message, "That position is not on the board")
            return
        self.fail()

# TODO: captures? clocks?

if __name__ == "__main__":
    unittest.main()


