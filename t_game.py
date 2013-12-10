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
                "Freddo versus Sam\n9x9\nstandard rules\n")

    def test_make_game_header2(self):
        rules = Rules(13, "tournament")
        game = Game(rules, Player("Hansel"), Player("Gretel"))
        self.assertEquals(game.game_header(),
                "Hansel versus Gretel\n13x13\ntournament rules\n")

    def test_override_game_from_header(self):
        rules = Rules(13, "tournament")
        g = Game(rules, Player("Hansel"), Player("Gretel"))
        s = "Freddo versus Sam\n9x9\nstandard rules\nMore Stuff\n"

        the_rest = g.configure_from_str(s)

        self.assertEquals(g.size(), 9)
        self.assertEquals(g.get_player_name(1), "Freddo")
        self.assertEquals(g.get_player_name(2), "Sam")
        self.assertEquals(g.rules.type_str, "standard")
        self.assertEquals(the_rest, "More Stuff\n")

if __name__ == "__main__":
    unittest.main()



