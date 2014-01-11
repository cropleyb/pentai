#!/usr/bin/env python

import unittest

from rules import *
from game import *
from openings_db import *

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

if __name__ == "__main__":
    unittest.main()

