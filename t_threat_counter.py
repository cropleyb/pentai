#!/usr/bin/env python

import unittest

from board_strip import *
from utility_stats import *
from priority_filter import * # TODO: NullFilter

mapping = {
    " ": 0, # empty
    "B": 1, # Black
    "W": 2, # White
}

import pdb

def pattern_string_to_board_strip(occ_str):
    occs = 0
    letters = list(occ_str)
    letters.reverse()
    for occ in letters:
        occs *= 4
        occ_int = mapping[occ]
        occs += occ_int
    return occs

"""
    As with length counters, we need to subtract all the threats before
    the change to the position, and add them all after.
    We need to process all the groups of 4 that pass through the affected
    point.
"""
class SubStripCountingTest(unittest.TestCase):
    def setUp(self):
        self.threats = [0,0,0]
        self.us = UtilityStats(search_filter=PriorityFilter())
        self.threats = self.us.threats

    # Helper
    def process_threats_for_str(self, ss_str, ind, strip_min=0):
        occs = pattern_string_to_board_strip(ss_str)
        brd_size = len(ss_str)
        process_threats(occs, ind, strip_min, brd_size-1, self.us, 1)

    # Tests
    def test_count_empty(self):
        self.process_threats_for_str("    ", 3)
        self.assertEquals(self.threats, [0,0,0])

    def test_black_right(self):
        self.process_threats_for_str(" WW    ", 3)
        self.assertEquals(self.threats, [0,2,0])

    def test_white_right(self):
        self.process_threats_for_str("    BB ", 4)
        self.assertEquals(self.threats, [0,0,2])

    def test_black_and_white(self):
        self.process_threats_for_str(" BB WW ", 3)
        self.assertEquals(self.threats, [0,2,2])

    # Some non-threat cases
    def test_black_take_not_threat(self):
        self.process_threats_for_str("   BBW ", 3)
        self.assertEquals(self.threats, [0,0,0])

    def test_white_take_no_threat(self):
        self.process_threats_for_str("BWW    ", 3)
        self.assertEquals(self.threats, [0,0,0])

    def test_whatever(self):
        self.process_threats_for_str("   BW B", 3)
        self.assertEquals(self.threats, [0,0,0])
    
    def test_threat_spot_would_be_off_left(self):
        self.process_threats_for_str(" WW  ", 3, strip_min=1)
        self.assertEquals(self.threats, [0,0,0])

    def test_threat_spot_would_be_off_right(self):
        self.process_threats_for_str("     BB", 4)
        self.assertEquals(self.threats, [0,0,0])
    
    def test_zebra(self):
        self.process_threats_for_str("WBB WWB", 3)
        self.assertEquals(self.threats, [0,0,0])

    def test_zebra_below(self):
        self.process_threats_for_str("WBB WWB", 2)
        self.assertEquals(self.threats, [0,0,0])

    def test_gap(self):
        self.process_threats_for_str("  B B  ", 3)
        self.assertEquals(self.threats, [0,0,0])

if __name__ == "__main__":
    unittest.main()



