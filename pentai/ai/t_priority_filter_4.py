#!/usr/bin/env python

import unittest

from pentai.base.board import *
from pentai.ai.priority_filter_4 import *

class PriorityFilter4Test(unittest.TestCase):
    def setUp(self):
        self.pf4 = PriorityFilter4()
        self.pf4.set_our_colour(P1)

    def arc(self, colour, length, subtype, candidate_list, inc=1):
        #cl2 = [(i,0) for i in candidate_list]
        #print "Subtype in test is %s" % subtype
        self.pf4.add_or_remove_candidates(colour, length, subtype, candidate_list, inc)

    def set_captured_by(self, is_us, captured):
        self.pf4.captured[is_us] = captured

    def ar_take(self, *args, **kwargs):
        self.pf4.add_or_remove_take(*args, **kwargs)

    def ar_threat(self, *args, **kwargs):
        self.pf4.add_or_remove_threat(*args, **kwargs)

    def test_dont_start_in_the_middle_13(self):
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 0)

    def test_add_and_remove(self):
        self.arc(P1, 4, 0, (((3,4),0),) )
        self.arc(P1, 4, 0, (((3,4),0),), -1 )
        self.arc(P1, 3, 0, (((3,2),0),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,2))

    def test_iterate_over_our_four(self):
        self.arc(P1, 4, 0, (((3,4),0),) )
        self.arc(P1, 3, 2, (((3,2),2),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_one_of_their_fours(self):
        #st()
        self.arc(P2, 4, 0, (((3,4),0),) )
        self.ar_take(P1, (3,2))
        self.set_captured_by(True, 6)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(3,2))

    def test_two_of_their_fours_try_the_take(self):
        self.arc(P2, 4, 0, (((1,2),0),) )
        self.arc(P2, 4, 0, (((3,4),0),) )
        self.ar_take(P1, (3,2))
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,2))

    def test_two_of_their_fours_no_take(self):
        self.arc(P2, 4, 0, (((1,2),0),) )
        self.arc(P2, 4, 0, (((3,4),0),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        # It doesn't matter which one we choose, we're lost
        # Evaluating this node should give the result
        # But we need to choose one or the other

    def test_finish_capture_win(self):
        self.set_captured_by(True, 8)
        self.ar_take(P1, (1,2))
        self.arc(P2, 4, 0, (((3,4),0),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,2))

    def test_block_or_take_to_defend_capture_loss(self):
        self.set_captured_by(False, 8)
        self.ar_take(P1, (1,2))
        self.ar_take(P2, (3,4))
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 2)

    def test_iterate_over_own_win_only(self):
        self.arc(P2, 4, 0, (((1,5),0),) )
        self.arc(P1, 4, 0, (((3,4),0),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_block_their_four_only(self):
        self.arc(P2, 3, 0, (((1,5),0),) )
        self.arc(P2, 4, 0, (((3,4),0),) )
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_capture(self):
        self.pf4.add_or_remove_take(P1, (3,4))
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))

    def test_iterate_over_own_capture_first(self):
        self.pf4.add_or_remove_take(P1, (1,2))
        self.pf4.add_or_remove_take(P2, (3,4))
        l = list(self.pf4.get_iter(P2))
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0],(3,4))
        self.assertEquals(l[1],(1,2))

    def test_iterate_over_other_players_four_before_our_capture(self):
        self.pf4.add_or_remove_take(P2, (7,2))
        self.arc(P1, 4, 0, (((3,4),0),) )
        l = list(self.pf4.get_iter(P2))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(3,4))
        #self.assertEquals(l[1],(7,2))

    def test_iterate_block_only(self):
        self.arc(P2, 3, 2, (((1,5),2), ((2,4),1)) )
        self.pf4.add_or_remove_take(P1, (1,5))
        self.arc(P1, 4, 0, (((2,4),0),) )
        l = list(self.pf4.get_iter(P2))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(2,4))

    def test_iterate_over_capture(self):
        self.pf4.add_or_remove_take(P1, (1,5))
        l = list(self.pf4.get_iter(P2))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_iterate_over_their_capture_before_our_twos_in_order(self):
        self.arc(P1, 2, 1, (((2,4),0), ((4,6),2), ((5,7),1)) )
        self.pf4.add_or_remove_take(P2, (1,5))
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 4)
        self.assertEquals(l[0],(1,5))
        self.assertEquals(l[1],(4,6))
        self.assertEquals(l[2],(5,7))
        self.assertEquals(l[3],(2,4))

    def atest_iterate_over_their_three_before_our_threat(self):
        self.arc(P1, 3, 1, (((2,4),0), ((4,6),1)) )
        #self.pf4.add_or_remove_threat(P2, (1,5))
        self.arc(P2, (1,5))
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 3)
        threes = (2,4),(4,6)
        self.assertIn(l[0], threes)
        self.assertIn(l[1], threes)
        self.assertEquals(l[2],(1,5))
        
    def test_add_and_remove_length_candidate(self):
        self.arc(P1, 3, 2, (((2,4),1),((4,6),2)), inc=1)
        self.pf4.add_or_remove_threat(P1, (1,5))
        self.arc(P1, 3, 2, (((2,4),1),((4,6),2)), inc=-1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(1,5))

    def test_add_and_remove_capture_candidate(self):
        self.pf4.add_or_remove_take(P1, (1,5), inc=1)
        self.pf4.add_or_remove_take(P1, (1,5), inc=-1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 0)

    def test_add_and_remove_threat_candidate(self):
        self.pf4.add_or_remove_threat(P1, (1,5), inc=1)
        self.pf4.add_or_remove_threat(P1, (1,5), inc=-1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 0)

    def test_add_and_remove_length_candidate_from_diff_directions(self):
        self.arc(P1, 3, 2, (((2,4),2),((4,6),2),), inc=1)
        self.arc(P1, 3, 2, (((2,4),2),((3,3),2),), inc=1)
        self.arc(P1, 3, 2, (((2,4),2),((4,6),2),), inc=-1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 2)
        pair = ((2,4),(3,3),)
        self.assertIn(l[0], pair)
        self.assertIn(l[1], pair)

    def test_multiple_entries_searched_first(self):
        # TODO: Should be multiple entries for the same length, 
        # irrespective of subtype. ATM each subtype is grouped together.
        self.arc(P1, 3, 1, (((2,4),1),((4,6),1)), inc=1)
        self.arc(P1, 3, 1, (((2,4),1),((3,3),1)), inc=1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 3)
        self.assertEquals(l[0],(2,4))
        others = ((4,6), (3,3))
        self.assertIn(l[1], others)
        self.assertIn(l[2], others)

    def test_copy_is_deep(self):
        self.arc(P1, 3, 2, (((2,4),2),((3,3),1)), inc=1)
        self.arc(P1, 4, 0, (((3,3),0),), inc=1)
        bsc = self.pf4.copy()
        bsc.add_or_remove_candidates(P1, 4, 0, (((3,3),0),), inc=-1)
        # Modifying the descendant should not have affected the parent
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(l[0],(3,3))

    def atest_multiple_entries_searched_first2(self):
        self.arc(P1, 3, ((4,6),(5,6),), inc=1)
        self.arc(P1, 3, ((9,6),(10,6),), inc=1)
        self.arc(P1, 3, ((5,6),(9,6),), inc=1)
        self.arc(P2, 2, ((7,8),(8,8),(10,8)), inc=1)
        self.arc(P2, 2, ((8,8),(10,8),(12,8)), inc=1)
        self.arc(P2, 2, ((10,8),(12,8),(13,8)), inc=1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 4)
        first_pair = ((5,6), (9,6))
        self.assertIn(l[0], first_pair)
        self.assertIn(l[1], first_pair)

    def test_pointless_positions_ignored_gracefully(self):
        self.arc(P1, 4, 0, (((4,6),0),), inc=1)
        self.arc(P1, 4, 0, (((5,7),0),), inc=1)
        self.arc(P1, 4, 0, (((4,6),0),), inc=-1)
        l = list(self.pf4.get_iter(P1))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(5,7))

if __name__ == "__main__":
    unittest.main()

