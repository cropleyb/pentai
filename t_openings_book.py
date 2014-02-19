#!/usr/bin/env python

import unittest
import random

from rules import *
from game import *
from openings_book import *
from games_mgr import *
from player import *



class ATOTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(9, "standard")
        self.games_mgr = GamesMgr(prefix="test_")
        p1 = Player("BC")
        p2 = Player("Whoever")
        self.game = self.games_mgr.create_game(self.rules, p1, p2)
        self.o_mgr = OpeningsBook(self.games_mgr, prefix="test_")

    def tearDown(self):
        for fn in (["test_s_9_openings.pkl", "test_id_map.pkl",
                    "test_unfinished.pkl", "test_s_9.pkl"]):
            try:
                os.unlink(fn)
            except:
                pass

    def load_moves_and_set_win(self, moves, winner=BLACK):
        self.game.load_moves(moves)
        self.game.current_state.set_won_by(winner)

    def test_no_suggestions(self):
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.o_mgr.get_move_games(g2))

        self.assertEquals(len(moves), 0)

    def test_add_initial_position(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_position(self.game, 1)
        self.games_mgr.save(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.o_mgr.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((4,4), [self.game]))

    def test_add_first_white_move(self):
        # Force assymetry
        self.load_moves_and_set_win("1. (2,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (2,3)")

        moves = list(self.o_mgr.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,3), [self.game]))

    def test_suggest_second_black_move(self):
        self.load_moves_and_set_win(
                "1. (1,4)\n2. (2,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (1,4)\n2. (2,3)")

        moves = list(self.o_mgr.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,4), [self.game]))

    def test_add_second_white_move(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4, 4)\n2. (3, 3)\n3. (3, 4)")

        moves = list(self.o_mgr.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), [self.game]))

    def test_find_two_alternatives(self):
        self.load_moves_and_set_win("1. (1,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_game(self.game)
        
        # Add a second historical game
        sg = Game(self.rules, Player("Shazam"), Player("Floff"))
        sg.load_moves("1. (1,3)\n2. (2,2)\n3. (6,4)") # etc.
        sg.current_state.set_won_by(WHITE)
        self.o_mgr.add_game(sg)
        
        load_game = Game(self.rules, Player("Now1"), Player("Now2"))
        game_str = '1. (1,3)'
        load_game.load_moves(game_str)
        
        move_games = list(self.o_mgr.get_move_games(load_game))

        self.assertEquals(len(move_games), 2)
        move_games.sort()
        self.assertEquals(move_games,
                [((2,2), [sg]),
                 ((3,3), [self.game])])

    def test_find_a_symmetrical_starting_move(self):
        self.load_moves_and_set_win("1. (3,4)")

        self.o_mgr.add_game(self.game)
        lg = Game(self.rules, Player("Now1"), Player("Now2"))

        moves = list(self.o_mgr.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertIn(moves[0][0], [(3, 4), (4,3), (5,4), (4,5)])

    # !./t_openings_db.py ATOTest.test_find_move_from_symmetrical_game
    def test_find_move_from_symmetrical_game(self):
        self.load_moves_and_set_win(
                "1. (1,2)\n2. (2,3)\n3. (1,4)\n4. (5,4)")
        self.o_mgr.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (7, 2)\n2. (6, 3)\n3. (7, 4)")

        moves = list(self.o_mgr.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3, 4), [self.game]))

    def run_and_check_moves(self, moves_str, last_move_pos):
        self.game.load_moves(moves_str)
        self.game.make_move(last_move_pos)
        self.game.current_state.set_won_by(BLACK)
        self.o_mgr.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves(moves_str)

        moves = list(self.o_mgr.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], (last_move_pos, [self.game]))

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

    ################################
    # Persistence tests

    # ! ./t_openings_book.py ATOTest.test_persist_position
    def test_persist_position(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_position(self.game, 1, sync=True)

        games_mgr = GamesMgr(prefix="test_")
        o_mgr2 = OpeningsBook(games_mgr=games_mgr, prefix="test_")

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((4,4), [self.game]))

    def test_persist_position_lookup_different_size(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_position(self.game, 1, sync=True)

        games_mgr = GamesMgr(prefix="test_")
        o_mgr2 = OpeningsBook(games_mgr=games_mgr, prefix="test_")

        rules2 = Rules(13, "standard")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 0)

    def test_persist_position_lookup_different_rules_type(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.o_mgr.add_position(self.game, 1, sync=True)

        games_mgr = GamesMgr(prefix="test_")
        o_mgr2 = OpeningsBook(games_mgr=games_mgr, prefix="test_")

        rules2 = Rules(9, "5 in a row")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 0)

    def test_only_save_finished_games(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", EMPTY)
        self.o_mgr.add_game(self.game)

        games_mgr = GamesMgr(prefix="test_")
        o_mgr2 = OpeningsBook(games_mgr=games_mgr, prefix="test_")

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 0)

    def test_only_save_games_once(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")

        self.o_mgr.add_game(self.game)
        try:
            self.o_mgr.add_game(self.game)
        except OpeningsBookDuplicateException:
            return
        self.fail()

    # TODO: rules types delegation tests

if __name__ == "__main__":
    unittest.main()

