#!/usr/bin/env python

import unittest
from openings_filter import *
from board import *

import pdb

class MockGame:
    def __init__(self, wc):
        self.winner_colour = wc

    def winner(self):
        return self.winner_colour

class OpeningsFilterTest(unittest.TestCase):
    def setUp(self):
        self.of = OpeningsFilter()

    def test_no_moves_available_suggest_nothing(self):
        move_games = []
        self.of.set_move_games(move_games)
        move = self.of.get_a_good_move(BLACK)
        self.assertEquals(move, None)

    def multiple_tries(self, tries, func, *args, **kwargs):
        answers = {}
        for iters in range(tries):
            answer = func(*args, **kwargs)
            if not answers.has_key(answer):
                answers[answer] = 1
            else:
                answers[answer] += 1
        return answers

    def test_one_favourable_game_mostly_doesnt_fall_through(self):
        g1 = MockGame(BLACK)
        move_games = [((4,4), (g1,))]
        self.of.set_move_games(move_games)

        answers = self.multiple_tries(1000, self.of.get_a_good_move, BLACK)

        self.assertGreater(answers[(4,4)], 600)
        self.assertGreater(answers[None], 100)

    def test_one_unfavourable_game_mostly_falls_through(self):
        g1 = MockGame(WHITE)
        move_games = [((4,4), (g1,))]
        self.of.set_move_games(move_games)

        answers = self.multiple_tries(1000, self.of.get_a_good_move, BLACK)

        self.assertGreater(answers[(4,4)], 100)
        self.assertGreater(answers[None], 600)

    def test_one_move_equal_standings(self):
        g1 = MockGame(BLACK)
        g2 = MockGame(WHITE)
        move_games = [((4,4), (g1,g2))]
        self.of.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.of.get_a_good_move, BLACK)

        self.assertGreater(answers[(4,4)], 350)
        self.assertGreater(answers[None], 350)

    def test_two_moves_one_good_one_bad(self):
        g1 = MockGame(BLACK)
        g2 = MockGame(WHITE)
        move_games = [((4,4), (g1,)), ((3,4),(g2,))]
        self.of.set_move_games(move_games)
        answers = self.multiple_tries(1000, self.of.get_a_good_move, BLACK)

        self.assertGreater(answers[(4,4)], 650)
        self.assertGreater(answers[(3,4)], 50)
        self.assertGreater(answers[None], 100)

if __name__ == "__main__":
    unittest.main()

