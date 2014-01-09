#!/usr/bin/env python

import unittest

from rules import *
from game import *
from openings_db import *

class ATOTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(9, "standard")
        self.game = self.create_game()
        self.game.load_moves("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.game.current_state.set_won_by(BLACK)

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
        self.game.load_moves("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")

        o_db.add_game(self.game)

        self.assertEquals(len(o_db.get_games(self.rules)), 1)

    def test_add_initial_position(self):
        o_db = OpeningsDb()

        o_db.add_position(self.game, 1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = o_db.get_moves(g2)
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((4,4), self.game))

    def test_add_first_white_move(self):
        o_db = OpeningsDb()

        o_db.add_position(self.game, 1)
        o_db.add_position(self.game, 2)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4,4)")

        moves = o_db.get_moves(g2)

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,3), self.game))

    def test_find_two_alternatives(self):
        o_db = OpeningsDb()

        o_db.add_position(self.game, 1)
        o_db.add_position(self.game, 2)

        sg = Game(self.rules, Player("Shazam"), Player("Floff"))
        sg.load_moves("1. (4,4)\n2. (2,2)\n3. (6,4)") # etc.
        self.game.current_state.set_won_by(WHITE)
        o_db.add_position(sg, 1)
        o_db.add_position(sg, 2)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (4,4)")

        moves = o_db.get_moves(lg)

        self.assertEquals(len(moves), 2)
        self.assertEquals(moves[0], ((3,3), self.game), ((2,2), sg))

if __name__ == "__main__":
    unittest.main()

