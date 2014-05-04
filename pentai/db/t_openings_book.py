#!/usr/bin/env python

import unittest
import random

from pentai.base.rules import *
from pentai.base.game import *
from openings_book import *
from pentai.db.games_mgr import *
from pentai.base.player import *
import pentai.db.test_db as test_db

class ATOTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "standard")
        self.games_mgr = GamesMgr()
        p1 = Player("BC")
        p2 = Player("Whoever")
        self.game = self.games_mgr.create_game(self.rules, p1, p2)
        self.ob = OpeningsBook(self.games_mgr)

    def tearDown(self):
        test_db.clear_all()

    def load_moves_and_set_win(self, moves, winner=BLACK, game=None):
        if not game:
            game = self.game
        game.load_moves(moves)
        game.current_state.set_won_by(winner)

    def test_no_suggestions(self):
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 0)

    # ./t_openings_book.py ATOTest.test_add_initial_position
    def test_add_initial_position(self):
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n3. (9,10)\n4. (11,10)")
        self.ob.add_position(self.game, 1)
        self.games_mgr.save(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((10,10), [self.game]))

    def test_add_first_white_move(self):
        self.load_moves_and_set_win("1. (7,8)\n2. (8,8)\n")
        self.ob.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (7,8)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((8,8), [self.game]))


    # Up to here (converting to 19x19 default)
    def test_suggest_second_black_move(self):
        #st()
        self.load_moves_and_set_win(
                "1. (1,4)\n2. (2,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (1,4)\n2. (2,3)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((3,4), [self.game]))

    def test_add_second_white_move(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4, 4)\n2. (3, 3)\n3. (3, 4)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), [self.game]))

    def test_find_two_alternatives(self):
        self.load_moves_and_set_win("1. (1,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game)
        
        # Add a second historical game
        sg = Game(self.rules, Player("Shazam"), Player("Floff"))
        sg.load_moves("1. (1,3)\n2. (2,2)\n3. (6,4)") # etc.
        sg.current_state.set_won_by(WHITE)
        self.ob.add_game(sg)
        
        load_game = Game(self.rules, Player("Now1"), Player("Now2"))
        game_str = '1. (1,3)'
        load_game.load_moves(game_str)
        
        move_games = list(self.ob.get_move_games(load_game))

        self.assertEquals(len(move_games), 2)
        move_games.sort()
        self.assertEquals(move_games,
                [((2,2), [sg]),
                 ((3,3), [self.game])])

    #! ./pentai/db/t_openings_book.py ATOTest.test_find_move_from_translated_game
    def test_find_move_from_translated_game(self):
        # Shifted one to the right
        self.load_moves_and_set_win(
                "1. (6,7)\n2. (10,10)\n3. (8,9)\n4. (6,5)")
        self.ob.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (7,7)\n2. (11,10)\n3. (9,9)")

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((7, 5), [self.game]))

    # !./t_openings_db.py ATOTest.test_find_move_from_symmetrical_game
    def test_find_move_from_symmetrical_game(self):
        self.load_moves_and_set_win(
                "1. (6,7)\n2. (7,8)\n3. (6,10)\n4. (10,9)")
        self.ob.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (12, 7)\n2. (11, 8)\n3. (12, 10)")

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((8, 9), [self.game]))

    def run_and_check_moves(self, moves_str, last_move_pos):
        self.game.load_moves(moves_str)
        self.game.make_move(last_move_pos)
        self.game.current_state.set_won_by(BLACK)
        self.ob.add_game(self.game)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves(moves_str)

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], (last_move_pos, [self.game]))

    # !pentai/db/t_openings_book.py ATOTest.test_NW
    def test_NW(self):
        #st()
        self.run_and_check_moves("1. (0,18)\n2. (1,18)", (2,18))

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
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n3. (9,10)\n4. (11,10)")
        self.ob.add_position(self.game, 1, sync=True)

        games_mgr = GamesMgr()
        o_mgr2 = OpeningsBook(games_mgr=games_mgr)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((10,10), [self.game]))

    def test_persist_position_lookup_different_size(self):
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n3. (9,10)\n4. (11,9)")
        self.ob.add_game(self.game)

        games_mgr = GamesMgr()
        o_mgr2 = OpeningsBook(games_mgr=games_mgr)

        rules2 = Rules(13, "standard")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        self.load_moves_and_set_win("1. (7,7)\n2. (6,6)\n3. (6,7)", game=g2)
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((8,6), [self.game]))

    def test_persist_position_lookup_different_rules_type(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game)

        games_mgr = GamesMgr()
        o_mgr2 = OpeningsBook(games_mgr=games_mgr)

        rules2 = Rules(19, "5 in a row")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)", game=g2)
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), [self.game]))

    def test_only_save_finished_games(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", EMPTY)
        self.ob.add_game(self.game)

        games_mgr = GamesMgr()
        o_mgr2 = OpeningsBook(games_mgr=games_mgr)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 0)

    # Failing?
    def test_only_save_games_once(self):
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")

        self.ob.add_game(self.game)
        #st()
        try:
            self.ob.add_game(self.game)
        except OpeningsBookDuplicateException:
            return
        self.fail()

    # Disabled but noteworthy...
    def atest_symmetrical_moves_are_accumulated(self):
        # This is failing because the current position is what is standardised,
        # not the position after the suggested moves.
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4,4)\n2. (5,5)\n3. (3,4)\n4. (5,4)")
        g2.current_state.set_won_by(BLACK)
        self.ob.add_game(g2)

        g3 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g3.load_moves("1. (4, 4)\n")

        moves = list(self.ob.get_move_games(g3))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), [self.game]))

class TranslationalSymmetryTest(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "5")
        self.games_mgr = GamesMgr()
        p1 = Player("BC")
        p2 = Player("Whoever")
        self.game = self.games_mgr.create_game(self.rules, p1, p2)
        self.ob = OpeningsBook(self.games_mgr)

    def tearDown(self):
        test_db.clear_all()

    def load_moves_and_set_win(self, moves, winner=BLACK):
        self.game.load_moves(moves)
        self.game.current_state.set_won_by(winner)

    # ! kivy pentai/db/t_openings_book.py ATOTest.test_translation_away_from_edges
    def test_translation_away_from_edges(self):
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n")
        self.ob.add_game(self.game)

        # Pick a spot slightly away from the centre
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (8,8)\n")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        possibilities = [((7,7), [self.game]),
                         ((9,7), [self.game]),
                         ((9,9), [self.game]),
                         ((7,9), [self.game])]
        self.assertIn(moves[0], possibilities)

    # TODO: rules types delegation tests

if __name__ == "__main__":
    unittest.main()

