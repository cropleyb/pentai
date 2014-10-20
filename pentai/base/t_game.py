#!/usr/bin/env python

import unittest

from pentai.base.game import *
from pentai.base.rules import *
from pentai.base.player import *

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

    def test_load_finished_game(self):
        rules = Rules(19, "tournament")
        game = Game(rules, Player("Kelvin"), Player("Bruce"))
        game.load_moves("1. (9,9)\n2. (10, 8)\n3. (12,9)\n4. (12,10)\n5. (11,9)\n6. (10,9)\n7. (10,10)\n8. (13,9)\n9. (11,11)\n10. (12,12)\n11. (8,8)\n12. (7,7)\n13. (11,8)\n14. (12,11)\n15. (12,13)\n16. (14,8)\n17. (11,9)\n18. (12,8)\n19. (12,9)\n20. (9,11)\n21. (10,7)\n22. (13,10)\n23. (11,12)\n24. (15,7)\n25. (11,13)\n26. (16,6)\n")
        self.assertEquals(game.get_won_by(), P2)

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
        rem = g.tick(P1, 1)
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(rem, 179)

    def test_tick_white(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        rem = g.tick(P2, 2)
        self.assertEquals(g.remaining_time(P2), 178)
        self.assertEquals(rem, 178)

    def test_tick_black_twice(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        rem = g.tick(P1, 1)
        self.assertEquals(g.remaining_time(P1), 178)
        self.assertEquals(rem, 178)

    def test_take_back_1_returns_to_orig_time_control(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        g.make_move((0,0))
        g.go_backwards_one()
        self.assertEquals(g.remaining_time(P1), 179)

    def test_take_back_1_from_2_returns_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 180)
        g.make_move((0,0))
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 180)
        g.tick(P2, 2)
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 178)
        g.make_move((1,1))
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 178)
        g.go_backwards_one()
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 178)

    def test_tick_before_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 180)

    def test_second_tick_before_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        g.tick(P1, 1)
        self.assertEquals(g.remaining_time(P1), 178)
        self.assertEquals(g.remaining_time(P2), 180)

    def test_tick_then_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        g.make_move((0,0))
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 180)

    def test_tick_move_tick(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        g.make_move((0,0))
        g.tick(P2, 1)
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 179)

    #! ./pentai/base/t_game.py GameTest.test_take_back_first_move
    def test_take_back_first_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        #st()
        g.tick(P1, 1)
        g.make_move((0,0))
        g.tick(P2, 1)
        g.go_backwards_one()
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 180)

    def test_take_back_first_move_then_redo_it(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.tick(P1, 1)
        g.make_move((0,0))
        g.tick(P2, .5)
        g.go_backwards_one()
        g.go_forwards_one()

        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 179.5)

    # ! ./pentai/base/t_game.py GameTest.test_undo_capture
    def test_undo_capture(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))
        g.make_move((1,0))
        g.make_move((0,0))
        g.make_move((2,0))
        g.make_move((3,0))
        board = g.get_board()
        self.assertEquals(board.get_occ((1,0)), EMPTY)
        self.assertEquals(board.get_occ((2,0)), EMPTY)

        g.go_backwards_one()
        self.assertEquals(board.get_occ((1,0)), P1)
        self.assertEquals(board.get_occ((2,0)), P1)

    def test_take_back_1_then_forwards_1_should_recall_start_of_current_move(self):
        rules = Rules(9, "standard", time_control=3)
        g = Game(rules, Player("BC"), Player("Whoever"))

        g.tick(P1, 1)
        g.make_move((0,0))

        g.tick(P2, 1)
        g.make_move((1,1))
        g.tick(P1, 1)

        g.go_backwards_one()
        self.assertEquals(g.remaining_time(P1), 179)
        self.assertEquals(g.remaining_time(P2), 179)

        g.go_forwards_one()
        self.assertEquals(g.remaining_time(P1), 178)
        self.assertEquals(g.remaining_time(P2), 179)

    def test_get_rating_from_player(self):
        rules = Rules(9, "standard")
        p1 = Player("P1")
        p1.set_rating(1179)
        p2 = Player("P2")
        g = Game(rules, p1, p2)
        self.assertEquals(g.get_rating(P1), 1179)

    def test_get_rating_from_game(self):
        rules = Rules(9, "standard")
        p1 = Player("P1")
        p2 = Player("P2")
        g = Game(rules, p1, p2)
        g.set_rating(P1, 1179)
        self.assertEquals(g.get_rating(P1), 1179)

    def test_win_far_corner(self):
        rules = Rules(19, "tournament")
        game = Game(rules, Player("Kelvin"), Player("Bruce"))
        game.load_moves("1. (9,9)\n2. (18,18)\n3. (3,5)\n4. (17,17)\n5. (6,3)\n6. (16,16)\n7. (11,1)\n8. (15,15)\n9. (8,6)\n10. (14,14)\n")
        self.assertEquals(game.get_won_by(), P2)

if __name__ == "__main__":
    unittest.main()

