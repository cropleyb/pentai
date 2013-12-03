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

if __name__ == "__main__":
    unittest.main()

