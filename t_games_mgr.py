#!/usr/bin/env python

import unittest

from game import *
from rules import *
from human_player import *
from games_mgr import *
from players_mgr import *

class GamesMgrTest(unittest.TestCase):
    def setUp(self):
        self.test_players_fn = 'test_players.pkl'
        self.test_game_fn = 'test_S_9.pkl' # Hacky but it works
        self.gm = GamesMgr("test_")

    def tearDown(self):
        for filename in [self.test_players_fn, self.test_game_fn,
                "test_unfinished.pkl", "test_id_map.pkl"]:
            try:
                os.unlink(filename)
            except OSError: pass

    def test_game_to_filename(self):
        rules = Rules(13, "tournament")
        g = self.gm.create_game(rules, Player("Freddo"), Player("Sam"))

        fn = self.gm.get_filename(g)
        self.assertEquals(fn, "test_t_13.pkl")

    def test_game_to_filename2(self):
        rules = Rules(19, "5 in a row")
        g = self.gm.create_game(rules, Player("Alpha"), Player("Romeo"))

        fn = self.gm.get_filename(g)
        self.assertEquals(fn, "test_5_19.pkl")

    def test_id_to_filename(self):
        rules = Rules(19, "5 in a row")
        g = self.gm.create_game(rules, Player("Freddo"), Player("Sam"))

        fn = self.gm.get_filename(g.get_game_id())
        self.assertEquals(fn, "test_5_19.pkl")

    def test_save_and_fetch_game(self):
        rules = Rules(9, "Standard")
        g = self.gm.create_game(rules, HumanPlayer("Someone"), HumanPlayer("Else"))
        g.make_move((5,3))
        self.gm.save(g)

        g2 = self.gm.get_game(g.get_game_id())

        self.assertNotEquals(g2, None)
        self.assertEquals(g2.__class__, game.Game)
        self.assertEquals(g2.move_history, [(5,3)])

    def test_no_such_game(self):
        rules = Rules(9, "Standard")
        g = Game(rules, HumanPlayer("The Thing"), HumanPlayer("Blomp"))
        g2 = self.gm.get_game(g.get_game_id())

        self.assertEquals(g2, None)

    def test_save_and_fetch_two_games(self):
        rules = Rules(9, "Standard")
        g1 = self.gm.create_game(rules, HumanPlayer("Alfredo"), HumanPlayer("Candice"))
        g1.make_move((5,3))
        self.gm.save(g1)
        g2 = self.gm.create_game(rules, HumanPlayer("Gertrude Smythe"), HumanPlayer("Tony-Basil"))
        g2.make_move((8,2))
        self.gm.save(g2)

        fg1 = self.gm.get_game(g1.get_game_id())
        self.assertNotEquals(fg1, None)
        self.assertEquals(fg1.move_history, [(5,3)])

        fg2 = self.gm.get_game(g2.get_game_id())
        self.assertNotEquals(fg2, None)
        self.assertEquals(fg2.move_history, [(8,2)])

    def test_save_unfinished_game_goes_to_unfinished_list(self):
        rules = Rules(9, "Standard")
        g1 = self.gm.create_game(rules, HumanPlayer("Glacier"), HumanPlayer("Slug"))
        g1.make_move((5,3))
        self.gm.save(g1)

        fg1 = self.gm.get_unfinished_game(g1.get_game_id())
        self.assertNotEquals(fg1, None)
        self.assertEquals(fg1.move_history, [(5,3)])

    def test_save_finished_game_doesnt_go_to_unfinished_list(self):
        rules = Rules(9, "Standard")
        g1 = self.gm.create_game(rules, HumanPlayer("Glacier"), HumanPlayer("Slug"))
        g1.make_move((5,3))
        g1.set_won_by(BLACK)
        self.gm.save(g1)

        fg1 = self.gm.get_unfinished_game(g1.get_game_id())
        self.assertEquals(fg1, None)

    def test_newly_finished_game_is_removed_from_unfinished_list(self):
        rules = Rules(9, "Standard")
        g1 = self.gm.create_game(rules, HumanPlayer("Glacier"), HumanPlayer("Slug"))
        g1.make_move((5,3))
        self.gm.save(g1)
        g1.make_move((6,3))
        g1.set_won_by(BLACK)
        self.gm.save(g1)

        fg1 = self.gm.get_unfinished_game(g1.get_game_id())
        self.assertEquals(fg1, None)

    ############################

    def test_unpack_game_without_db(self):
        rules = Rules(9, "Standard")
        g1 = self.gm.create_game(rules, HumanPlayer("Nadia"),
                                        HumanPlayer("Roberto"))
        g1.make_move((6,3))
        self.gm.save(g1)

        fg = self.gm.get_game(g1.get_game_id())
        self.assertEquals(fg, g1)

if __name__ == "__main__":
    unittest.main()



