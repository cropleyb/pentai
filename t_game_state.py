#!/usr/bin/env python

import unittest

from game_state import *
from player import *
from rules import *
from game import *

class GameStateTest(unittest.TestCase):
    def setUp(self):
        self.setUpWithOverrides(
                size=5,
                player1=HumanPlayer("Fred"),
                player2=HumanPlayer("Wilma"))

    def setUpWithOverrides(self, size=5, player1=None, player2=None, rules_str="standard"):
        rules = Rules(size, rules_str)
        self.game = Game(rules, player1, player2)

    def test_create_game_state_move_one(self):
        gs = GameState(self.game)
        self.assertEquals(gs.get_move_number(), 1)
        self.assertEquals(gs.get_captured(0), 0)
        self.assertEquals(gs.get_captured(1), 0)

    def test_make_one_move(self):
        gs = GameState(self.game)
        gs.make_move(Move(Pos(2,4)))
        self.assertEquals(gs.get_move_number(), 2)
        self.assertEquals(gs.get_captured(0), 0)
        self.assertEquals(gs.get_captured(1), 0)

    """ 
    def make_move(self, move):
        move_pos = move.pos
        if self.board.get_occ(move_pos) > 0:
            raise IllegalMoveException()

        # Place a stone
        my_colour = self.to_move()
        self.board.set_occ(move_pos, my_colour)
        board_size = self.board.get_size()

        # Process captures
        for direction in DIRECTIONS:
            clrs = self.board.get_occs_in_a_line(move_pos, direction, 4)
            if clrs == [1, 2, 2, 1] or clrs == [2, 1, 1, 2]:
                capture_pos1 = move_pos.shift(direction, 1)
                capture_pos2 = move_pos.shift(direction, 2)
                # Remove stones
                self.set_colour(capture_pos1, 0)
                self.set_colour(capture_pos2, 0)
                # Keep track of capture count
                self.captured[my_colour] += 1

        # Check for a win (TEMP)
        for direction in DIRECTIONS:
            l = 1
            while l < 5:
                test_pos = move_pos.shift(direction, l)
                if test_pos[0] < 0 or \
                   test_pos[0] >= board_size or \
                   test_pos[1] < 0 or \
                   test_pos[1] >= board_size:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.board.get_occ(test_pos)
                if next_col != my_colour:
                    break
                l += 1
            m = -1
            while m > -5:
                test_pos = move_pos.shift(direction, m)
                if test_pos[0] < 0 or \
                   test_pos[0] >= board_size or \
                   test_pos[1] < 0 or \
                   test_pos[1] >= board_size:
                    # Other end of a potential line is off the edge of the board
                    break
                next_col = self.board.get_occ(test_pos)
                if next_col != my_colour:
                    break
                m -= 1
            total_line_length = 1 + l - m
            if total_line_length >= 5:
                self.won_by = my_colour

    def to_move(self):
        return not self.move_number % 2

    def successors(self):
        succ = []
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                pos = Pos(x, y)
                action = Move(pos)
                try:
                    succ.append((action, State(self, action)))
                except IllegalMoveException:
                    pass
        return succ

    def utility(self, player):
        # 5+ in a row or 5+ captured = infinity
        if self.captured[0] == 5 or self.won_by == 1:
            return alpha_beta.infinity
        if self.captured[1] == 5 or self.won_by == 2:
            return -alpha_beta.infinity
        return self.captured[0] - self.captured[1]

    def score(self):
        return self.utility(None)
    """ 


if __name__ == "__main__":
    unittest.main()



