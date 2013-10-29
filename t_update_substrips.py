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


class GameTest(unittest.TestCase):
    def test_count_empty(self):
        pattern = pattern_string_to_int_list("         ")
        us_counter = LengthCounter()
        them_counter = LengthCounter()
        templates = add_substrips(pattern, us_counter, them_counter)
        self.assertEquals(us_counter.tup(), (0,0,0,0,0))
        self.assertEquals(them_counter.tup(), (0,0,0,0,0))

    def test_count_single_us(self):
        pattern = pattern_string_to_int_list("    U    ")
        us_counter = LengthCounter()
        them_counter = LengthCounter()
        #pdb.set_trace()
        templates = add_substrips(pattern, us_counter, them_counter)
        self.assertEquals(us_counter.tup(), (5,0,0,0,0))
        self.assertEquals(them_counter.tup(), (0,0,0,0,0))

    def test_count_single_them(self):
        pattern = pattern_string_to_int_list("    T    ")
        us_counter = LengthCounter()
        them_counter = LengthCounter()
        templates = add_substrips(pattern, us_counter, them_counter)
        self.assertEquals(us_counter.tup(), (0,0,0,0,0))
        self.assertEquals(them_counter.tup(), (5,0,0,0,0))

    def test_count_single_us_at_end(self):
        pattern = pattern_string_to_int_list("U        ")
        us_counter = LengthCounter()
        them_counter = LengthCounter()
        templates = add_substrips(pattern, us_counter, them_counter)
        self.assertEquals(us_counter.tup(), (1,0,0,0,0))
        self.assertEquals(them_counter.tup(), (0,0,0,0,0))


if __name__ == "__main__":
    unittest.main()



