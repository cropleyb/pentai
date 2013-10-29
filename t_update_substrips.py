#!/usr/bin/env python

import unittest

import pdb

from update_substrips import *

def pattern_string_to_int_list(occ_str):
    ret = []
    mapping = {
        " ": 0, # empty
        "U": 1, # us
        "T": 2, # them
    }
    for occ in occ_str:
        occ_int = mapping[occ]
        ret.append(occ_int)
    return ret


class SubStripCountingTest(unittest.TestCase):
    def setUp(self):
        self.us_counter = LengthCounter()
        self.them_counter = LengthCounter()

    # Helper
    def add_substrips_for_str(self, ss_str):
        pattern = pattern_string_to_int_list(ss_str)
        add_substrips(pattern, self.us_counter, self.them_counter)

    def test_count_empty(self):
        self.add_substrips_for_str("         ")
        self.assertEquals(self.us_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_single_us(self):
        self.add_substrips_for_str("    U    ")
        self.assertEquals(self.us_counter.tup(), (5,0,0,0,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_single_them(self):
        self.add_substrips_for_str("    T    ")
        self.assertEquals(self.us_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.them_counter.tup(), (5,0,0,0,0))

    def test_count_single_us_at_end(self):
        self.add_substrips_for_str("U        ")
        self.assertEquals(self.us_counter.tup(), (1,0,0,0,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_open_three(self):
        self.add_substrips_for_str("   UUU   ")
        self.assertEquals(self.us_counter.tup(), (0,2,3,0,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_open_four(self):
        self.add_substrips_for_str("  UUUU   ")
        self.assertEquals(self.us_counter.tup(), (0,1,2,2,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_closed_four(self):
        self.add_substrips_for_str(" TUUUU   ")
        self.assertEquals(self.us_counter.tup(), (0,1,1,1,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

    def test_count_open_three_with_space_and_single_them(self):
        self.add_substrips_for_str(" T UUU   ")
        self.assertEquals(self.us_counter.tup(), (0,1,2,0,0))
        self.assertEquals(self.them_counter.tup(), (0,0,0,0,0))

if __name__ == "__main__":
    unittest.main()



