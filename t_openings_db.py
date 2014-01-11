#!/usr/bin/env python

import unittest

from rules import *
from game import *
from openings_db import *

import pdb

def load_moves_and_set_win(game, moves, winner):
    game.load_moves(moves)
    game.current_state.set_won_by(winner)

class ATOTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(9, "standard")
        self.game = self.create_game()

    def create_game(self):
        # Game to be recorded
        game = Game(self.rules, Player("BC"), Player("Whoever"))
        return game


    def test_empty_db(self):
        o_db = OpeningsDb()
        games = o_db.get_games(self.rules)
        self.assertEquals(len(games), 0)

    def test_add_9_game(self):
        o_db = OpeningsDb()
        self.rules = Rules(9, "standard")
        self.game = self.create_game()

        o_db.add_game(self.game)

        self.assertEquals(len(o_db.get_games(self.rules)), 1)

    def test_add_13_game(self):
        o_db = OpeningsDb()
        self.rules = Rules(13, "standard")
        self.game = Game(self.rules, Player("BC"), Player("Whoever"))
        load_moves_and_set_win(self.game, "1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", BLACK)

        o_db.add_game(self.game)

        self.assertEquals(len(o_db.get_games(self.rules)), 1)

    def test_no_suggestions(self):
        o_db = OpeningsDb()
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(o_db.get_moves(g2))

        self.assertEquals(len(moves), 0)

    def test_add_initial_position(self):
        o_db = OpeningsDb()
        load_moves_and_set_win(self.game, "1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", BLACK)
        o_db.add_position(self.game, 1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(o_db.get_moves(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((4,4), self.game))

    def test_add_first_white_move(self):
        o_db = OpeningsDb()
        # Force assymetry
        load_moves_and_set_win(self.game, "1. (2,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)", BLACK)
        o_db.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (2,3)")

        moves = list(o_db.get_moves(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,3), self.game))

    def test_suggest_second_black_move(self):
        o_db = OpeningsDb()
        load_moves_and_set_win(self.game,
                "1. (1,4)\n2. (2,3)\n3. (3,4)\n4. (5,4)", BLACK)
        o_db.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (1,4)\n2. (2,3)")

        moves = list(o_db.get_moves(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,4), self.game))

    def test_add_second_white_move(self):
        o_db = OpeningsDb()
        load_moves_and_set_win(self.game, "1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", BLACK)
        o_db.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4, 4)\n2. (3, 3)\n3. (3, 4)")

        moves = list(o_db.get_moves(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), self.game))

    def test_find_two_alternatives(self):
        o_db = OpeningsDb()
        load_moves_and_set_win(self.game, "1. (1,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)", BLACK)
        o_db.add_game(self.game)
        
        # Add a second historical game
        sg = Game(self.rules, Player("Shazam"), Player("Floff"))
        sg.load_moves("1. (1,3)\n2. (2,2)\n3. (6,4)") # etc.
        self.game.current_state.set_won_by(WHITE)
        o_db.add_game(sg)
        
        load_game = Game(self.rules, Player("Now1"), Player("Now2"))
        game_str = '1. (1,3)'
        load_game.load_moves(game_str)
        
        moves = list(o_db.get_moves(load_game))

        self.assertEquals(len(moves), 2)
        self.assertEquals(moves, [((3,3), self.game), ((2,2), sg)])

    def test_find_a_symmetrical_starting_move(self):
        o_db = OpeningsDb()
        self.game.load_moves("1. (3,4)")

        o_db.add_game(self.game)
        lg = Game(self.rules, Player("Now1"), Player("Now2"))

        moves = list(o_db.get_moves(lg))

        self.assertEquals(len(moves), 1)
        self.assertIn(moves[0][0], [(3, 4), (4,3), (5,4), (4,5)])

    # !./t_openings_db.py ATOTest.test_find_move_from_symmetrical_game
    def test_find_move_from_symmetrical_game(self):
        o_db = OpeningsDb()
        self.game.load_moves("1. (1,2)\n2. (2,3)\n3. (1,4)\n4. (5,4)")
        o_db.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (7, 2)\n2. (6, 3)\n3. (7, 4)")

        moves = list(o_db.get_moves(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3, 4), self.game))

    def run_and_check_moves(self, moves_str, last_move_pos):
        o_db = OpeningsDb()
        self.game.load_moves(moves_str)
        self.game.make_move(last_move_pos)
        o_db.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves(moves_str)

        moves = list(o_db.get_moves(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], (last_move_pos, self.game))

    def test_NW(self):
        self.run_and_check_moves("1. (0,8)\n2. (1,8)", (2,8))

    def test_NE(self):
        self.run_and_check_moves("1. (8,8)\n2. (7,8)", (6,8))

    def test_EN(self):
        self.run_and_check_moves("1. (8,8)\n2. (8,7)", (8,6))

    def test_ES(self):
        self.run_and_check_moves("1. (8,0)\n2. (8,1)", (8,2))

    def test_SE(self):
        self.run_and_check_moves("1. (8,0)\n2. (7,0)", (6,0))

    def test_SW(self):
        self.run_and_check_moves("1. (0,0)\n2. (1,0)", (2,0))

    def test_WS(self):
        self.run_and_check_moves("1. (0,0)\n2. (0,1)", (0,2))

    def test_WN(self):
        self.run_and_check_moves("1. (0,8)\n2. (0,7)", (0,6))

    # TODO random game replay?

if __name__ == "__main__":
    unittest.main()

