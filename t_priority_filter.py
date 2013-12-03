#!/usr/bin/env python

import unittest
from priority_filter import *
from board import *

import pdb

class PriorityFilterTest(unittest.TestCase):
    def test_start_in_the_middle_13(self):
        b = Board(13)
        pf = PriorityFilter(b)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(6,6))

    def test_iterate_over_one_four(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_colour_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_candidates(WHITE, 4, ((1,5),))
        pf.report_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_higher_priority_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_candidates(WHITE, 3, ((1,5),))
        pf.report_candidates(WHITE, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_capture_threat(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_threat(BLACK, (3,4))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_capture_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_threat(BLACK, (1,2))
        pf.report_threat(WHITE, (3,4))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,2))

    def test_iterate_over_other_players_four_before_our_capture(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_threat(WHITE, (7,2))
        pf.report_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(7,2))

    def test_iterate_over_other_players_capture_before_our_threes(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.report_candidates(BLACK, 3, ((3,4),(1,5)))
        pf.report_threat(WHITE, (7,2))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(7,2))
        our_threes = ((3,4),(1,5))
        self.assertIn(l[1], our_threes)
        self.assertIn(l[2], our_threes)


if __name__ == "__main__":
    unittest.main()

