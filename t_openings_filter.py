#!/usr/bin/env python

import unittest

from mock import Mock
from openings_filter import *
from board import *

import pdb

class MockFoundGame:
    """ This one is for games that have been found in the opening book
    """
    def __init__(self, wc):
        self.winner_colour = wc

    def winner(self):
        return self.winner_colour

class OpeningsFilterTest(unittest.TestCase):
    def setUp(self):
        self.om = Mock()
        self.of = OpeningsFilter(self.om)
        self.msg = Mock()
        self.to_move_colour = BLACK
        self.msg.mockAddReturnValues(to_move_colour=self.to_move_colour)

    def set_move_games(self, move_games):
        self.om.mockAddReturnValues(get_move_games=move_games)

    def test_no_moves_available_suggest_nothing(self):
        move_games = []
        self.set_move_games(move_games)
        move = self.of.get_a_good_move(self.msg)
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
        g1 = MockFoundGame(BLACK)
        move_games = [((4,4), (g1,))]
        self.set_move_games(move_games)

        answers = self.multiple_tries(1000, self.msg)

        self.assertGreater(answers[(4,4)], 600)
        self.assertGreater(answers[None], 100)

    def test_one_unfavourable_game_mostly_falls_through(self):
        g1 = MockFoundGame(WHITE)
        move_games = [((4,4), (g1,))]
        self.set_move_games(move_games)

        answers = self.multiple_tries(1000, self.msg)

        self.assertGreater(answers[(4,4)], 100)
        self.assertGreater(answers[None], 600)

    def test_one_move_equal_standings(self):
        g1 = MockFoundGame(BLACK)
        g2 = MockFoundGame(WHITE)
        move_games = [((4,4), (g1,g2))]
        self.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.msg)

        self.assertGreater(answers[(4,4)], 350)
        self.assertGreater(answers[None], 350)

    def test_two_moves_one_good_one_bad(self):
        g1 = MockFoundGame(BLACK)
        g2 = MockFoundGame(WHITE)
        move_games = [((4,4), (g1,)), ((3,4),(g2,))]
        self.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.msg)

        self.assertGreater(answers[(4,4)], 650)
        self.assertGreater(answers[(3,4)], 50)
        self.assertGreater(answers[None], 100)

if __name__ == "__main__":
    unittest.main()

