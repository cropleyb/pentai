#!/usr/bin/env python

import unittest

from pentai.base.board import *
from pentai.ai.priority_filter import *

class PriorityFilterTest(unittest.TestCase):
    def setUp(self):
        self.pf = PriorityFilter()

    def arc(self, colour, length, candidate_list, inc=1):
        cl2 = [(i,0) for i in candidate_list]
        self.pf.add_or_remove_candidates(colour, length, cl2, inc)

    def get_iter(self, colour, *args, **kwargs):
        return list(self.pf.get_iter(colour, None, *args, **kwargs))

    def test_dont_start_in_the_middle_13(self):
        l = self.get_iter(P1)
        self.assertEquals(len(l), 0)

    def test_iterate_over_one_four(self):
        self.arc(P1, 4, ((3,4),))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_colour_first(self):
        self.arc(P2, 4, ((1,5),))
        self.arc(P1, 4, ((3,4),))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_higher_priority_first(self):
        self.arc(P2, 3, ((1,5),))
        self.arc(P2, 4, ((3,4),))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_capture(self):
        self.pf.add_or_remove_take(P1, (3,4))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_capture_first(self):
        self.pf.add_or_remove_take(P1, (1,2))
        self.pf.add_or_remove_take(P2, (3,4))
        l = self.get_iter(P2)
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,2))

    def test_iterate_over_other_players_four_before_our_capture(self):
        self.pf.add_or_remove_take(P2, (7,2))
        self.arc(P1, 4, ((3,4),))
        l = self.get_iter(P2)
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(7,2))

    def test_iterate_over_other_players_capture_before_our_threes(self):
        self.arc(P1, 3, ((3,4),(1,5)))
        self.pf.add_or_remove_take(P2, (7,2))
        l = self.get_iter(P2)
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(7,2))
        our_threes = ((3,4),(1,5))
        self.assertIn(l[1], our_threes)
        self.assertIn(l[2], our_threes)

    def test_iterate_capture_three_and_four_triple_once(self):
        self.arc(P2, 3, ((1,5),(2,4)))
        self.pf.add_or_remove_take(P1, (1,5))
        self.arc(P1, 4, ((2,4),))
        l = self.get_iter(P2)
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(2,4))
        self.assertEquals(l[1],(1,5))

    def test_iterate_over_capture(self):
        self.pf.add_or_remove_take(P1, (1,5))
        l = self.get_iter(P2)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_iterate_over_their_capture_before_our_two(self):
        self.arc(P1, 2, ((2,4),(4,6),(5,7)))
        self.pf.add_or_remove_take(P2, (1,5))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 4)
        self.assertEquals(l[0],(1,5))
        twos = (2,4),(4,6),(5,7)
        self.assertIn(l[1], twos)
        self.assertIn(l[2], twos)
        self.assertIn(l[3], twos)

    def test_iterate_over_their_three_before_our_threat(self):
        self.arc(P1, 3, ((2,4),(4,6),))
        self.pf.add_or_remove_threat(P2, (1,5))
        l = self.get_iter(P1)
        self.assertEquals(len(l), 3)
        threes = (2,4),(4,6)
        self.assertIn(l[0], threes)
        self.assertIn(l[1], threes)
        self.assertEquals(l[2],(1,5))
        
    def test_add_and_remove_length_candidate(self):
        self.arc(P1, 3, ((2,4),(4,6),), inc=1)
        self.pf.add_or_remove_threat(P1, (1,5))
        self.arc(P1, 3, ((2,4),(4,6),), inc=-1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_add_and_remove_capture_candidate(self):
        self.pf.add_or_remove_take(P1, (1,5), inc=1)
        self.pf.add_or_remove_take(P1, (1,5), inc=-1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 0)

    def test_add_and_remove_threat_candidate(self):
        self.pf.add_or_remove_threat(P1, (1,5), inc=1)
        self.pf.add_or_remove_threat(P1, (1,5), inc=-1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 0)

    def test_add_and_remove_length_candidate_from_diff_directions(self):
        self.arc(P1, 3, ((2,4),(4,6),), inc=1)
        self.arc(P1, 3, ((2,4),(3,3),), inc=1)
        self.arc(P1, 3, ((2,4),(4,6),), inc=-1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 2)
        pair = ((2,4),(3,3),)
        self.assertIn(l[0], pair)
        self.assertIn(l[1], pair)

    def test_multiple_entries_searched_first(self):
        self.arc(P1, 3, ((2,4),(4,6),), inc=1)
        self.arc(P1, 3, ((2,4),(3,3),), inc=1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(2,4))
        others = ((4,6), (3,3))
        self.assertIn(l[1], others)
        self.assertIn(l[2], others)

    def test_min_priority4(self):
        self.arc(P1, 3, ((2,4),(3,3),), inc=1)
        self.arc(P1, 4, ((3,3),), inc=1)
        l = self.get_iter(P1, min_priority=4)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,3))

    def test_min_priority2(self): # TODO
        self.arc(P1, 1, ((2,4),(3,3),), inc=1)
        self.pf.add_or_remove_threat(P1, (3,3))
        l = self.get_iter(P1, min_priority=2)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,3))

    def atest_copy_only_copies_high_priority(self):
        # TODO?
        self.arc(P1, 3, ((2,4),(3,3),), inc=1)
        self.arc(P1, 4, ((3,3),), inc=1)
        pfc = self.pf.copy(min_priority=4)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,3))

    def test_copy_is_deep(self):
        self.arc(P1, 3, ((2,4),(3,3),), inc=1)
        self.arc(P1, 4, ((3,3),), inc=1)
        pfc = self.pf.copy()
        pfc.add_or_remove_candidates(P1, 4, [((3,3),0)], inc=-1)
        # Modifying the descendant should not have affected the parent
        l = self.get_iter(P1)
        self.assertEquals(l[0],(3,3))

    def test_multiple_entries_searched_first2(self):
        self.arc(P1, 3, ((4,6),(5,6),), inc=1)
        self.arc(P1, 3, ((9,6),(10,6),), inc=1)
        self.arc(P1, 3, ((5,6),(9,6),), inc=1)
        self.arc(P2, 2, ((7,8),(8,8),(10,8)), inc=1)
        self.arc(P2, 2, ((8,8),(10,8),(12,8)), inc=1)
        self.arc(P2, 2, ((10,8),(12,8),(13,8)), inc=1)
        l = self.get_iter(P1)
        self.assertGreater(len(l), 5)
        first_pair = ((5,6), (9,6))
        self.assertIn(l[0], first_pair)
        self.assertIn(l[1], first_pair)

    def test_pointless_positions_ignored_gracefully(self):
        self.arc(P1, 4, ((4,6),), inc=1)
        self.arc(P1, 4, ((5,7),), inc=1)
        self.arc(P1, 4, ((4,6),), inc=-1)
        l = self.get_iter(P1)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(5,7))

    def test_skip_tried(self):
        self.arc(P1, 4, ((4,6),), inc=1)
        self.arc(P1, 4, ((5,7),), inc=1)
        self.arc(P1, 4, ((6,8),), inc=1)
        tried = set([(4,6),(6,8)])
        l = self.get_iter(P1, tried=tried)
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(5,7))

if __name__ == "__main__":
    unittest.main()

