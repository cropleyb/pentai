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

    def test_tick_black(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        rem = g.tick(BLACK, 1)
        self.assertEquals(g.remaining_time(BLACK), 179)
        self.assertEquals(rem, 179)

    def test_tick_white(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        rem = g.tick(WHITE, 2)
        self.assertEquals(g.remaining_time(WHITE), 178)
        self.assertEquals(rem, 178)

    def test_tick_black_twice(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(BLACK, 1)
        rem = g.tick(BLACK, 1)
        self.assertEquals(g.remaining_time(BLACK), 178)
        self.assertEquals(rem, 178)

    def test_take_back_1_returns_to_orig_time_control(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(BLACK, 1)
        g.make_move((0,0))
        g.go_backwards_one()
        self.assertEquals(g.remaining_time(BLACK), 180)

    def test_take_back_1_from_2_returns_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(BLACK, 1)
        g.make_move((0,0))
        g.tick(WHITE, 2)
        g.make_move((1,1))
        g.go_backwards_one()
        self.assertEquals(g.remaining_time(BLACK), 179)
        self.assertEquals(g.remaining_time(WHITE), 180)

if __name__ == "__main__":
    unittest.main()



