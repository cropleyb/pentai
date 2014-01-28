#!/usr/bin/env python

import unittest

from game import *
from rules import *
from player import *

class GameTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_moves(self):
        rules = Rules(9, "standard")
        game = Game(rules, Player("Freddo"), Player("Sam"))
        game.load_moves("1. (4, 4)\n2. (3, 3)\n")
        self.assertEquals(game.get_move_number(), 3)

    def test_make_game_header(self):
        rules = Rules(9, "standard")
        game = Game(rules, Player("Freddo"), Player("Sam"))
        self.assertEquals(game.game_header(),
                "Freddo versus Sam\n9x9\nStandard rules\n")

    def test_make_game_header2(self):
        rules = Rules(13, "tournament")
        game = Game(rules, Player("Hansel"), Player("Gretel"))
        self.assertEquals(game.game_header(),
                "Hansel versus Gretel\n13x13\nTournament rules\n")

    def test_override_game_from_header(self):
        rules = Rules(13, "Tournament")
        g = Game(rules, Player("Hansel"), Player("Gretel"))
        s = "Freddo versus Sam\n9x9\nStandard rules\nMore Stuff\n"

        the_rest = g.configure_from_str(s)

        self.assertEquals(g.size(), 9)
        self.assertEquals(g.get_player_name(1), "Freddo")
        self.assertEquals(g.get_player_name(2), "Sam")
        self.assertEquals(g.rules.get_type_name(), "Standard")
        self.assertEquals(the_rest, "More Stuff\n")

    def test_go_to_move_back(self):
        rules = Rules(9, "standard")
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.load_moves("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.assertEquals(g.get_move_number(), 5)
        g.go_to_move(2)
        self.assertEquals(g.get_move_number(), 2)
        
    def test_go_to_move_back_then_forward(self):
        rules = Rules(9, "standard")
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.load_moves("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        g.go_to_move(2)
        g.go_to_move(5)
        self.assertEquals(g.get_move_number(), 5)
        
    def test_go_to_move_back_then_make_a_new_move(self):
        rules = Rules(9, "standard")
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.load_moves("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        g.go_to_move(2)
        g.make_move((0,0))
        self.assertEquals(g.get_move_number(), 3)
        self.assertEquals(g.get_move(1), (4,4))
        self.assertEquals(g.get_move(2), (0,0))

if __name__ == "__main__":
    unittest.main()



