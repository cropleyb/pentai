#!/usr/bin/env python

import unittest

from mock import Mock
from openings_mover import *
from board import *

import pdb

class MockPlayer:
    def get_rating(self):
        return 1

class MockPreservedGame:
    """ This one is for games that have been found in the opening book
    """
    def __init__(self, wc, rf):
        self.won_by = wc
        self.rf = rf

    def get_won_by(self):
        return self.won_by

    def get_rating(self, colour):
        return self.rf

class OpeningsMoverTest(unittest.TestCase):
    def setUp(self):
        self.mom = Mock() # Mock Openings Manager
        self.msg = Mock() # Mock Search Game
        self.of = OpeningsMover(self.mom, self.msg)
        self.msg.mockAddReturnValues(to_move_colour=BLACK)
        self.player = MockPlayer()

    def set_move_games(self, move_games):
        self.mom.mockAddReturnValues(get_move_games=move_games)

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
        g1 = MockPreservedGame(BLACK, 1)
        move_games = [((4,4), (g1,))]
        self.set_move_games(move_games)

        answers = self.multiple_tries(1000, self.player)

        self.assertGreater(answers[(4,4)], 600)
        self.assertGreater(answers[None], 100)

    def test_one_move_equal_standings(self):
        g1 = MockPreservedGame(BLACK, 1)
        g2 = MockPreservedGame(WHITE, 1)
        move_games = [((4,4), (g1,g2))]
        self.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.player)

        self.assertGreater(answers[(4,4)], 350)
        self.assertGreater(answers[None], 350)

    def test_two_moves_one_good_one_bad(self):
        g1 = MockPreservedGame(BLACK, 1)
        g2 = MockPreservedGame(WHITE, 1)
        move_games = [((4,4), (g1,)), ((3,4),(g2,))]
        self.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.player)

        self.assertGreater(answers[(4,4)], 650)
        self.assertGreater(answers[(3,4)], 50)
        self.assertGreater(answers[None], 100)

if __name__ == "__main__":
    unittest.main()

