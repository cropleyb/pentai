#!/usr/bin/env python

import unittest
from search_filter import *

import pdb

class SearchFilterTest(unittest.TestCase):
    def test_initial_constraint(self):
        i = FilterIterator(13)
        l = list(i.get_iter())
        self.assertEquals(len(l), 5*5)
        self.assertEquals(l[0],(6,6))
        self.assertIn((8,8),l[-4:])

    def test_set_left_min(self):
        i = FilterIterator(13)
        i.widen((4,6))
        l = list(i.get_iter())
        self.assertEquals(len(l), 7*5)

    def test_set_right_max(self):
        i = FilterIterator(13)
        i.widen((7,6))
        l = list(i.get_iter())
        self.assertEquals(len(l), 6*5)

    def test_set_lower_min(self):
        i = FilterIterator(13)
        i.widen((6,2))
        l = list(i.get_iter())
        self.assertEquals(len(l), 9*5)

    '''
    def test_right_number_of_positions_for_big_board(self):
        i = (19)
        l = list(i.get_iter())
        self.assertEquals(len(l), 19 * 19)

    def test_centre_first(self):
        i = PosIterator(13)
        l = list(i.get_iter())
        self.assertEquals(l[0], (6,6))

    def test_corners_last(self):
        i = PosIterator(13)
        l = list(i.get_iter())
        corners = ((0,0), (0,12), (12,12), (12,0))
        self.assertIn(l[-1], corners)
        self.assertIn(l[-2], corners)
        self.assertIn(l[-3], corners)
        self.assertIn(l[-4], corners)

    def test_centre_first_big(self):
        i = PosIterator(19)
        l = list(i.get_iter())
        self.assertEquals(l[0], (9,9))

    def test_corners_last_big(self):
        i = PosIterator(19)
        l = list(i.get_iter())
        corners = ((0,0), (0,18), (18,18), (18,0))
        self.assertIn(l[-1], corners)
        self.assertIn(l[-2], corners)
        self.assertIn(l[-3], corners)
        self.assertIn(l[-4], corners)
    '''

if __name__ == "__main__":
    unittest.main()

