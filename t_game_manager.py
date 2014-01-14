#!/usr/bin/env python

import unittest

from game import *
from rules import *
from human_player import *
from game_manager import *

class GameManagerTest(unittest.TestCase):
    def setUp(self):
        self.gm = GameManager("test_players.pkl", "test_game_manager.pkl")

    def test_game_to_filename(self):
        rules = Rules(13, "tournament")
        g = self.gm.create_game(rules, Player("Freddo"), Player("Sam"))

        fn = self.gm.get_filename(g)
        self.assertEquals(fn, "t_13.pkl")

    def test_game_to_filename2(self):
        rules = Rules(19, "5 in a row")
        g = self.gm.create_game(rules, Player("Alpha"), Player("Romeo"))

        fn = self.gm.get_filename(g)
        self.assertEquals(fn, "5_19.pkl")

    def test_id_to_filename(self):
        rules = Rules(19, "5 in a row")
        g = self.gm.create_game(rules, Player("Freddo"), Player("Sam"))

        fn = self.gm.get_filename(g.get_game_id())
        self.assertEquals(fn, "5_19.pkl")

    def test_save_and_fetch_game(self):
        rules = Rules(9, "Standard")
        g = self.gm.create_game(rules, HumanPlayer("Someone"), HumanPlayer("Else"))
        self.gm.save(g)

        g2 = self.gm.get_game(g.get_game_id())

        self.assertNotEquals(g2, None)
        self.assertEquals(g2.__class__, game.Game)

    # TODO No such game


if __name__ == "__main__":
    unittest.main()



