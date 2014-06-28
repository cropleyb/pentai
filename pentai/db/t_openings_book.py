#!/usr/bin/env python

import unittest
import random
import sys

from pentai.base.rules import *
from pentai.base.game import *
import openings_book as ob_m
import misc_db as m_m
from pentai.db.games_mgr import *
from pentai.base.player import *
import pentai.db.test_db as tdb_m

def print_func():
    pass
    #print sys._getframe(1).f_code.co_name

class ATOTest(unittest.TestCase):
    def setUp(self):
        tdb_m.init()
        self.rules = Rules(19, "standard")
        games_mgr = GamesMgr()
        p1 = Player("BC")
        p2 = Player("Whoever")
        self.game = games_mgr.create_game(self.rules, p1, p2)
        self.ob = ob_m.OpeningsBook()

    def tearDown(self):
        tdb_m.clear_all()
        tdb_m.delete_test_db()
        ob_m.instance = None
        m_m.the_instance = None

    def load_moves_and_set_win(self, moves, winner=P1, game=None):
        if not game:
            game = self.game
        game.load_moves(moves)
        game.current_state.set_won_by(winner)

    def test_no_suggestions(self):
        print_func()
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 0)

    # ./t_openings_book.py ATOTest.test_add_initial_position
    def atest_add_initial_position(self):
        print_func()
        # This works when debugged?!
        #st()
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n3. (9,10)\n4. (11,10)")
        self.ob.add_position(self.game, 1, P1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (10,10))

    def atest_add_first_white_move(self):
        print_func()
        self.load_moves_and_set_win("1. (7,8)\n2. (8,8)\n")
        self.ob.add_game(self.game, P1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (7,8)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertIn(moves[0][0], [(8,8), (6,8), (7,9), (6,8)])
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    def test_suggest_second_black_move(self):
        print_func()
        self.load_moves_and_set_win(
                "1. (9,9)\n2. (10,8)\n3. (11,9)\n4. (13,9)")
        self.ob.add_game(self.game, P1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (9,9)\n2. (10,8)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertIn(moves[0][0], [(11,9), (9,7)])
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    # Up to here (converting to 19x19 default)
    def test_add_second_white_move(self):
        print_func()
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game, P1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4, 4)\n2. (3, 3)\n3. (3, 4)")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (5,4))
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    def test_find_two_alternatives(self):
        print_func()
        self.load_moves_and_set_win("1. (1,3)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game, P1)
        
        # Add a second historical game
        sg = Game(self.rules, Player("Shazam"), Player("Floff"))
        sg.game_id = 13
        sg.load_moves("1. (1,3)\n2. (2,2)\n3. (6,4)") # etc.
        sg.current_state.set_won_by(P2)
        self.ob.add_game(sg, P2)
        
        load_game = Game(self.rules, Player("Now1"), Player("Now2"))
        game_str = '1. (1,3)'
        load_game.load_moves(game_str)
        
        move_games = list(self.ob.get_move_games(load_game))

        self.assertEquals(len(move_games), 2)
        move_games.sort()
        self.assertEquals(move_games[0][0], (2,2))
        self.assertEquals(move_games[0][1], [0, 1, 1000, 1000])
        self.assertEquals(move_games[1][0], (3,3))
        self.assertEquals(move_games[1][1], [1, 0, 1000, 1000])

    #! ./pentai/db/t_openings_book.py ATOTest.test_find_move_from_translated_game
    def test_find_move_from_translated_game(self):
        #print __name__
        #print sys._getframe().f_code.co_name
        print_func()
        # Shifted one to the right
        self.load_moves_and_set_win(
                "1. (6,7)\n2. (10,10)\n3. (8,9)\n4. (6,5)")
        self.ob.add_game(self.game, P1)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (7,7)\n2. (11,10)\n3. (9,9)")

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (7, 5))
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    # !./t_openings_db.py ATOTest.test_find_move_from_symmetrical_game
    def test_find_move_from_symmetrical_game(self):
        print_func()
        self.load_moves_and_set_win(
                "1. (6,7)\n2. (7,8)\n3. (6,10)\n4. (10,9)")
        self.ob.add_game(self.game, P1)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves("1. (12, 7)\n2. (11, 8)\n3. (12, 10)")

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (8, 9))
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    def run_and_check_moves(self, moves_str, last_move_pos):
        self.game.rules.type_char = 't'
        self.game.load_moves(moves_str)
        self.game.make_move(last_move_pos)
        self.game.current_state.set_won_by(P1)
        self.ob.add_game(self.game, P1)

        lg = Game(self.rules, Player("Now1"), Player("Now2"))
        lg.load_moves(moves_str)

        moves = list(self.ob.get_move_games(lg))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], last_move_pos)
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    # !pentai/db/t_openings_book.py ATOTest.test_NW
    def test_NW(self):
        print_func()
        self.run_and_check_moves("1. (0,18)\n2. (1,18)", (2,18))

    def test_NE(self):
        print_func()
        self.run_and_check_moves("1. (8,8)\n2. (7,8)", (6,8))

    def test_EN(self):
        print_func()
        self.run_and_check_moves("1. (8,8)\n2. (8,7)", (8,6))

    def test_ES(self):
        print_func()
        self.run_and_check_moves("1. (8,0)\n2. (8,1)", (8,2))

    def test_SE(self):
        print_func()
        self.run_and_check_moves("1. (8,0)\n2. (7,0)", (6,0))

    def test_SW(self):
        print_func()
        self.run_and_check_moves("1. (0,0)\n2. (1,0)", (2,0))

    def test_WS(self):
        print_func()
        self.run_and_check_moves("1. (0,0)\n2. (0,1)", (0,2))

    def test_WN(self):
        print_func()
        self.run_and_check_moves("1. (0,8)\n2. (0,7)", (0,6))

    # TODO random game replay?

    ################################
    # Persistence tests

    # ! ./t_openings_book.py ATOTest.test_persist_position
    def test_persist_position(self):
        print_func()
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n3. (9,10)\n4. (11,10)")
        self.ob.add_position(self.game, 1, P1)

        o_mgr2 = ob_m.OpeningsBook()

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertIn(moves[0][0], [(8,8), (8,10), (10,8), (10,10)])
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    def atest_persist_position_lookup_different_size(self):
        # Don't use different sized game lookups for now
        print_func()
        self.load_moves_and_set_win("1. (9,9)\n2. (8,8)\n3. (8,9)\n4. (10,8)")
        self.ob.add_game(self.game, P1)

        o_mgr2 = ob_m.OpeningsBook()

        rules2 = Rules(13, "standard")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        self.load_moves_and_set_win("1. (7,7)\n2. (6,6)\n3. (6,7)", game=g2)
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (8,6))
        self.assertEquals(moves[0][1], [1, 0, 1000, 1000])

    def test_safe_size_candidate_board_smaller(self):
        print_func()
        our_rules = Rules(19, "standard")
        our_game = Game(our_rules, Player("Alpha"), Player("Beta"))
        cand_rules = Rules(13, "standard")
        cand_game = Game(cand_rules, Player("Psycho"), Player("Smith"))

        ob = ob_m.OpeningsBook()

        self.assertTrue(ob.safe_move((0,0), our_game, 13))
        self.assertTrue(ob.safe_move((12,12), our_game, 13))

    def test_safe_size_candidate_board_same(self):
        print_func()
        our_rules = Rules(19, "standard")
        our_game = Game(our_rules, Player("Alpha"), Player("Beta"))
        cand_rules = Rules(19, "standard")
        cand_game = Game(cand_rules, Player("Psycho"), Player("Smith"))

        ob = ob_m.OpeningsBook()

        self.assertTrue(ob.safe_move((0,0), our_game, 19))
        self.assertTrue(ob.safe_move((18,18), our_game, 19))

    def test_safe_size_candidate_board_bigger(self):
        print_func()
        our_rules = Rules(13, "standard")
        our_game = Game(our_rules, Player("Alpha"), Player("Beta"))
        cand_rules = Rules(19, "standard")
        cand_game = Game(cand_rules, Player("Psycho"), Player("Smith"))

        ob = ob_m.OpeningsBook()

        self.assertTrue(ob.safe_move((4,4), our_game, 19))
        self.assertTrue(ob.safe_move((8,8), our_game, 19))

        self.assertFalse(ob.safe_move((3,4), our_game, 19))
        self.assertFalse(ob.safe_move((4,3), our_game, 19))
        self.assertFalse(ob.safe_move((9,8), our_game, 19))
        self.assertFalse(ob.safe_move((8,9), our_game, 19))

    def test_persist_position_lookup_different_rules_type(self):
        print_func()
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game, P1)

        o_mgr2 = ob_m.OpeningsBook()

        rules2 = Rules(19, "5 in a row")
        g2 = Game(rules2, Player("Alpha"), Player("Beta"))
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)", game=g2)
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0][0], (5,4))

    def test_only_save_finished_games(self):
        print_func()
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)", EMPTY)
        self.ob.add_game(self.game, EMPTY)

        o_mgr2 = ob_m.OpeningsBook()

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        moves = list(o_mgr2.get_move_games(g2))
        self.assertEquals(len(moves), 0)

    # Failing? Intermittently
    # python pentai/db/t_openings_book.py ATOTest.test_only_save_games_once
    def test_only_save_games_once(self):
        print_func()
        '''
        Second add:
        > /Users/cropleyb/Dropbox/pente/pentai/db/openings_book.py(81)add_position()
        -> arr = pos_slot.setdefault(standardised_move, ZL())
        (Pdb) pos_slot[standardised_move]
        *** KeyError: (4, 14)
        (Pdb) pos_slot
        {(4, 4): [1]}
        (Pdb) next_move
        (4, 4)
        (Pdb) standardised_move
        (4, 14)
        '''
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")

        #st()
        self.ob.add_game(self.game, P1)
        try:
            self.ob.add_game(self.game, P1)
        except OpeningsBookDuplicateException:
            return
        self.fail()

    # Disabled but noteworthy...
    def atest_symmetrical_moves_are_accumulated(self):
        # This is failing because the current position is what is standardised,
        # not the position after the suggested moves.
        self.load_moves_and_set_win("1. (4,4)\n2. (3,3)\n3. (3,4)\n4. (5,4)")
        self.ob.add_game(self.game, P1)

        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (4,4)\n2. (5,5)\n3. (3,4)\n4. (5,4)")
        g2.current_state.set_won_by(P1)
        self.ob.add_game(g2, P1)

        g3 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g3.load_moves("1. (4, 4)\n")

        moves = list(self.ob.get_move_games(g3))

        self.assertEquals(len(moves), 1)
        self.assertEquals(moves[0], ((5,4), [self.game]))

class TranslationalSymmetryTest(unittest.TestCase):
    def setUp(self):
        tdb_m.init()
        self.rules = Rules(19, "5")
        games_mgr = GamesMgr()
        p1 = Player("BC")
        p2 = Player("Whoever")
        self.game = games_mgr.create_game(self.rules, p1, p2)
        self.ob = ob_m.OpeningsBook()

    def tearDown(self):
        tdb_m.clear_all()
        #tdb_m.delete_test_db()
        ob_m.instance = None
        m_m.the_instance = None

    def load_moves_and_set_win(self, moves, winner=P1):
        self.game.load_moves(moves)
        self.game.current_state.set_won_by(winner)
        self.game.game_id = random.randrange(10000)

    # ! kivy pentai/db/t_openings_book.py ATOTest.test_translation_away_from_edges
    def test_translation_away_from_edges(self):
        self.load_moves_and_set_win("1. (10,10)\n2. (9,9)\n")
        self.ob.add_game(self.game, P1)

        # Pick a spot slightly away from the centre
        g2 = Game(self.rules, Player("Alpha"), Player("Beta"))
        g2.load_moves("1. (8,8)\n")

        moves = list(self.ob.get_move_games(g2))

        self.assertEquals(len(moves), 1)
        possibilities = [(7,7), (9,7), (9,9), (7,9)]
        self.assertIn(moves[0][0], possibilities)

    # TODO: rules types delegation tests

class CirculateTest(unittest.TestCase):
    def tearDown(self):
        tdb_m.clear_all()
        ob_m.instance = None
        m_m.the_instance = None

    def test_circulate_array(self):
        a = range(20)
        aid = id(a)

        ob_m.circulate(a)

        self.assertEquals(a, range(10,20) + range(0,10))
        self.assertEquals(aid, id(a))

    def test_short_array(self):
        a = range(2)
        aid = id(a)

        ob_m.circulate(a)

        self.assertEquals(a, range(2))
        self.assertEquals(aid, id(a))

if __name__ == "__main__":
    unittest.main()

