#!/usr/bin/env python

import unittest

from take_counter import *

import pdb

mapping = {
    " ": 0, # empty
    "B": 1, # Black
    "W": 2, # White
}

def pattern_string_to_board_strip(occ_str):
    occs = 0
    letters = list(occ_str)
    letters.reverse()
    for occ in letters:
        occs *= 4
        occ_int = mapping[occ]
        occs += occ_int
    bs = BoardStrip(occs)
    return bs

"""
    As with length counters, we need to subtract all the takes before
    the change to the position, and add them all after.
    We need to process all the groups of 4 that pass through the affected
    point.
"""
class SubStripCountingTest(unittest.TestCase):
    def setUp(self):
        self.takes = [0,0,0]

    # Helper
    def process_takes_for_str(self, ss_str, ind):
        occs = pattern_string_to_board_strip(ss_str)
        brd_size = len(ss_str)
        process_takes(occs, ind, brd_size, self.takes, 1)

    # Tests
    def test_count_empty(self):
        self.process_takes_for_str("    ", 3)
        self.assertEquals(self.takes, [0,0,0])

    def test_black_right(self):
        self.process_takes_for_str("BWW    ", 3)
        self.assertEquals(self.takes, [0,1,0])

    def test_black_left(self):
        self.process_takes_for_str(" WWB   ", 1)
        self.assertEquals(self.takes,  [0,1,0])

    def test_white_right(self):
        self.process_takes_for_str("   WBB ", 4)
        self.assertEquals(self.takes, [0,0,1])

    def test_white_right_far(self):
        self.process_takes_for_str("   WBB ", 6)
        self.assertEquals(self.takes, [0,0,1])

    def test_white_left(self):
        self.process_takes_for_str(" BBW   ", 2) 
        self.assertEquals(self.takes, [0,0,1])

    def test_black_and_white(self):
        self.process_takes_for_str(" BBWW  ", 3)
        self.assertEquals(self.takes, [0,1,1])

    def test_two_takes(self):
        self.process_takes_for_str("WBB BBW", 3)
        self.assertEquals(self.takes, [0,0,2])

    def test_only_one_take_affected(self):
        self.process_takes_for_str("WBB BBW", 6)
        self.assertEquals(self.takes, [0,0,1])

    # Some non-take cases
    def test_black_bookended_no_take(self):
        self.process_takes_for_str("  WBBW ", 3)
        self.assertEquals(self.takes, [0,0,0])

    def test_white_bookended_no_take(self):
        self.process_takes_for_str("BWWB   ", 3)
        self.assertEquals(self.takes, [0,0,0])

    def test_whatever(self):
        self.process_takes_for_str("   BW B", 3)
        self.assertEquals(self.takes, [0,0,0])
    
    def test_capture_spot_would_be_off_left(self):
        self.process_takes_for_str("WWB    ", 1)
        self.assertEquals(self.takes, [0,0,0])

    def test_capture_spot_would_be_off_right(self):
        self.process_takes_for_str("   WBB", 3)
        self.assertEquals(self.takes, [0,0,0])
    
    def test_zebra(self):
        self.process_takes_for_str("WBB WWB", 3)
        self.assertEquals(self.takes, [0,1,1])

    def test_zebra_below(self):
        self.process_takes_for_str("WBB WWB", 2)
        self.assertEquals(self.takes, [0,0,1])

    def test_zebra_above(self):
        self.process_takes_for_str("WBB WWB", 4)
        self.assertEquals(self.takes, [0,1,0])

    def test_gap(self):
        self.process_takes_for_str("  W BB ", 3)
        self.assertEquals(self.takes, [0,0,0])

if __name__ == "__main__":
    unittest.main()



