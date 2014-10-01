#!/usr/bin/env python

import unittest

from pentai.base.defines import *
from pentai.base.rules import *
from pentai.gui.game_defaults import *

class TestGameDefaults(unittest.TestCase):
    def setUp(self):
        self.rules = Rules(19, "standard")
        self.gd = GameDefaults(self.rules)

    def play_game(self, p1, p2, rules=None):
        if rules == None:
            rules = self.rules
        self.gd.play_game(p1, p2, rules) 

    def test_initial(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        pn1 = self.gd.get_player(P1)
        pn2 = self.gd.get_player(P2)
        pt1 = self.gd.get_type(P1)
        pt2 = self.gd.get_type(P2)
        self.assertEquals(pn1, "BC")
        self.assertEquals(pn2, "Whoever")
        self.assertEquals(pt1, "Human")
        self.assertEquals(pt2, "AI")

    def test_initial2(self):
        self.play_game(("AI", "Samuel"), ("Human", "Bruce"))

        pn1 = self.gd.get_player(P1)
        pn2 = self.gd.get_player(P2)
        pt1 = self.gd.get_type(P1)
        pt2 = self.gd.get_type(P2)
        self.assertEquals(pn1, "Samuel")
        self.assertEquals(pn2, "Bruce")
        self.assertEquals(pt1, "AI")
        self.assertEquals(pt2, "Human")

    def test_rules(self):
        self.assertEquals(self.gd.get_size(), 19)
        self.assertEquals(self.gd.get_rules_type_name(), "Standard")

        new_rules = Rules(13, "Tournament")
        self.play_game(("AI", "Samuel"), ("Human", "Bruce"), new_rules)

        self.assertEquals(self.gd.get_size(), 13)
        self.assertEquals(self.gd.get_rules_type_name(), "Tournament")

    def test_change_p1_type_to_same(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_type(P1, "AI")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")

    def test_change_p1_type_to_same_as_p2(self):
        self.play_game(("Human", "BC"), ("AI", "Fred"))
        self.play_game(("Human", "BC"), ("AI", "Whoever"))
        #st()

        self.gd.set_type(P1, "AI")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Fred")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "AI")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Whoever")

    def test_change_p2_type_to_same_as_p1(self):
        self.play_game(("Human", "BC"), ("AI", "Fred"))
        self.play_game(("Human", "Anon"), ("AI", "Whoever"))

        self.gd.set_type(P2, "Human")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "BC")

    def test_change_both_types_from_human_to_ai(self):
        self.play_game(("AI", "Anon"), ("AI", "Whoever"))
        self.play_game(("Human", "BC"), ("Human", "Jespah"))

        self.gd.set_type(P1, "AI")
        self.gd.set_type(P2, "AI")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Anon")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "AI")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Whoever")

    def test_change_both_types_from_ai_to_human(self):
        self.play_game(("Human", "BC"), ("Human", "Jespah"))
        self.play_game(("AI", "Anon"), ("AI", "Whoever"))

        self.gd.set_type(P2, "Human")
        self.gd.set_type(P1, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "BC")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Jespah")

    def test_change_p1_type_and_back_again(self):
        self.play_game(("Human", "BC"), ("AI", "Fred"))
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_type(P1, "AI")
        self.gd.set_type(P1, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "BC")

    def test_change_p2_type_and_back_again(self):
        self.play_game(("Human", "Bruce"), ("Human", "BC"))
        self.play_game(("Human", "BC"), ("AI", "Fred"))
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_type(P2, "Human")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Bruce")

    def test_swap_types(self):
        self.play_game(("AI", "Deep Thunk"), ("Human", "Sandra"))
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_type(P1, "AI")
        self.gd.set_type(P2, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Whoever")
        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "BC")

    def test_set_type_insufficient_games(self):
        self.play_game(("Human", "BC"), ("Human", "Fred"))

        self.gd.set_type(P1, "AI")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "")

    def test_set_name(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_player(P1, "Tobiah")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Tobiah")

    def test_set_name_then_toggle_type_twice(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_player(P1, "Tobiah")
        self.gd.set_type(P1, "AI")
        self.gd.set_type(P1, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Tobiah")

    def test_set_name_then_toggle_both_player_types(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_player(P1, "Tobiah")
        self.gd.set_type(P1, "AI")
        self.gd.set_type(P2, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Whoever")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Tobiah")

    def test_game_with_same_players_doesnt_alter_candidate_players(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "BC")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "AI")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Whoever")

    def test_game_with_same_players_swapped_only_swaps_p1_p2(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))
        self.play_game(("AI", "Whoever"), ("Human", "BC"))

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Whoever")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "BC")

    def test_name_of_p2(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))

        self.gd.set_player(P2, "Deep Thunk")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "AI")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "Deep Thunk")

    def test_set_names_and_toggle_type(self):
        self.play_game(("Human", "BC"), ("AI", "Whoever"))
        self.play_game(("AI", "Deep Thunk"), ("AI", "Whoever"))

        self.gd.set_type(P1, "Human")
        self.gd.set_player(P1, "Bruce")
        self.gd.set_type(P2, "Human")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "Human")
        pn1 = self.gd.get_player(P1) # This is returning BC
        self.assertEquals(pn1, "Bruce")

        pt2 = self.gd.get_type(P2)
        self.assertEquals(pt2, "Human")
        pn2 = self.gd.get_player(P2)
        self.assertEquals(pn2, "BC")

    def test_set_ai_name_then_toggle_type(self):
        self.play_game(("AI", "Deep Thunk"), ("AI", "Whoever"))

        self.gd.set_player(P1, "Robo")
        self.gd.set_type(P1, "Human")
        self.gd.set_type(P1, "AI")

        pt1 = self.gd.get_type(P1)
        self.assertEquals(pt1, "AI")
        pn1 = self.gd.get_player(P1)
        self.assertEquals(pn1, "Robo")

    # TODO
    # Persistence tests

if __name__ == "__main__":
    unittest.main()

