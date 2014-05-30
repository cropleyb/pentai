#!/usr/bin/env python

import unittest
import random

from pentai.base.mock import Mock
from pentai.base.board import *
from pentai.db.op_pos import *
import pentai.ai.openings_mover as om_m

class MockPlayer:
    def get_rating(self):
        return 1000

class MockPreservedGame:
    """ This one is for games that have been found in the opening book
    """
    def __init__(self, wc, rating):
        self.won_by = wc
        self.rating = rating

    def get_size(self):
        return 9

    def get_won_by(self):
        return self.won_by

    def get_rating(self, colour):
        return self.rating

class OpeningsMoverTest(unittest.TestCase):
    def setUp(self):
        self.mob = Mock() # Mock Openings Book
        self.player = MockPlayer()
        self.msg = Mock() # Mock Base Game
        self.msg.mockAddReturnValues(size=9, is_live=True)
        self.msg.mockAddReturnValues(to_move_colour=BLACK)
        self.mabg = Mock() # Mock ABGame
        self.mabg.mockAddReturnValues(get_base_game=self.msg)
        self.of = om_m.OpeningsMover(self.mob, self.mabg)

        # Make the random tests deterministic for testing
        random.seed(1)

    def set_move_games(self, move_games):
        self.mob.mockAddReturnValues(get_move_games=move_games)

    def test_no_moves_available_suggest_nothing(self):
        move_games = []
        self.set_move_games(move_games)
        move = self.of.get_a_good_move(self.player)
        self.assertEquals(move, None)

    def multiple_tries(self, tries,  *args, **kwargs):
        answers = {}
        for iters in range(tries):
            answer = self.of.get_a_good_move(*args, **kwargs)
            if not answers.has_key(answer):
                answers[answer] = 1
            else:
                answers[answer] += 1
        return answers

    def test_one_favourable_game_mostly_doesnt_fall_through(self):
        move_games = [[(4,4), OpeningMoveGamesData([1,0,1000,1000])]]
        self.set_move_games(move_games)

        answers = self.multiple_tries(100, self.player)

        self.assertGreater(answers[(4,4)], 60)
        self.assertGreater(answers[None], 0)

    def test_one_move_equal_standings(self):
        move_games = [[(4,4), OpeningMoveGamesData([1,1,2000,1000])]]
        self.set_move_games(move_games)
        answers = self.multiple_tries(100, self.player)

        self.assertGreater(answers[(4,4)], 35)
        self.assertGreater(answers[None], 0)

    def test_two_moves_one_good_one_bad(self):
        move_games = [[(4,4), OpeningMoveGamesData([1,0,1000,1000])],
                      [(3,4), OpeningMoveGamesData([0,1,1000,1000])]]
        self.set_move_games(move_games)
        answers = self.multiple_tries(100, self.player)

        self.assertGreater(answers[(4,4)], 65)
        self.assertGreater(answers[(3,4)], 0)
        self.assertGreater(answers[None], 0)

    #! python pentai/ai/t_openings_mover.py OpeningsMoverTest.test_add_to_previously_seen
    def test_add_to_previously_seen(self):
        move_games = [[(4,4), OpeningMoveGamesData([1,0,1000,1000])],
                      [(3,4), OpeningMoveGamesData([0,1,1000,1000])]]
        self.set_move_games(move_games)

        seen = set()
        answer = self.of.get_a_good_move(self.player, seen=seen)

        self.assertIn((3,4), seen)
        self.assertIn((4,4), seen)
        self.assertNotIn((5,4), seen)

if __name__ == "__main__":
    unittest.main()

