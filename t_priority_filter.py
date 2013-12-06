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
        pf.add_or_remove_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_colour_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(WHITE, 4, ((1,5),))
        pf.add_or_remove_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_higher_priority_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(WHITE, 3, ((1,5),))
        pf.add_or_remove_candidates(WHITE, 4, ((3,4),))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_capture(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_capture(BLACK, (3,4))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_capture_first(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_capture(BLACK, (1,2))
        pf.add_or_remove_capture(WHITE, (3,4))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,2))

    def test_iterate_over_other_players_four_before_our_capture(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_capture(WHITE, (7,2))
        pf.add_or_remove_candidates(BLACK, 4, ((3,4),))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(7,2))

    def test_iterate_over_other_players_capture_before_our_threes(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((3,4),(1,5)))
        pf.add_or_remove_capture(WHITE, (7,2))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(7,2))
        our_threes = ((3,4),(1,5))
        self.assertIn(l[1], our_threes)
        self.assertIn(l[2], our_threes)

    def test_iterate_capture_three_and_four_triple_once(self):
        b = Board(13)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(WHITE, 3, ((1,5),(2,4)))
        pf.add_or_remove_capture(BLACK, (1,5))
        pf.add_or_remove_candidates(BLACK, 4, ((2,4),))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(2,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_capture(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_capture(BLACK, (1,5))
        l = list(pf.get_iter(WHITE))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_iterate_over_their_capture_before_our_two(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 2, ((2,4),(4,6),(5,7)))
        pf.add_or_remove_capture(WHITE, (1,5))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 4)
        self.assertEquals(l[0],(1,5))
        twos = (2,4),(4,6),(5,7)
        self.assertIn(l[1], twos)
        self.assertIn(l[2], twos)
        self.assertIn(l[3], twos)

    def test_iterate_over_their_three_before_our_threat(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),))
        pf.add_or_remove_threat(WHITE, (1,5))
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 3)
        threes = (2,4),(4,6)
        self.assertIn(l[0], threes)
        self.assertIn(l[1], threes)
        self.assertEquals(l[2],(1,5))
        
    def test_add_and_remove_length_candidate(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),), inc=1)
        pf.add_or_remove_threat(BLACK, (1,5))
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),), inc=-1)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_add_and_remove_capture_candidate(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_capture(BLACK, (1,5), inc=1)
        pf.add_or_remove_capture(BLACK, (1,5), inc=-1)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(4,4))

    def test_add_and_remove_threat_candidate(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_threat(BLACK, (1,5), inc=1)
        pf.add_or_remove_threat(BLACK, (1,5), inc=-1)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(4,4))

    def test_add_and_remove_length_candidate_from_diff_directions(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),), inc=1)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(3,3),), inc=1)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),), inc=-1)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 2)
        pair = ((2,4),(3,3),)
        self.assertIn(l[0], pair)
        self.assertIn(l[1], pair)

    def test_multiple_entries_searched_first(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(4,6),), inc=1)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(3,3),), inc=1)
        l = list(pf.get_iter(BLACK))
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(2,4))
        others = ((4,6), (3,3))
        self.assertIn(l[1], others)
        self.assertIn(l[2], others)

    def test_min_priority(self):
        b = Board(9)
        pf = PriorityFilter(b)
        pf.add_or_remove_candidates(BLACK, 3, ((2,4),(3,3),), inc=1)
        pf.add_or_remove_candidates(BLACK, 4, ((3,3),), inc=1)
        l = list(pf.get_iter(BLACK, min_priority=4))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,3))

if __name__ == "__main__":
    unittest.main()

