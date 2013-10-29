#!/usr/bin/env python

import unittest

import pdb

from pattern_conversion import *


class GameTest(unittest.TestCase):
    def test_convert_empty(self):
        pattern = "         "
        templates = convert_to_hash_value_list(pattern)

        self.assertEquals(len(templates), 1)
        self.assertTrue(0 in templates)

    def test_convert_to_1(self):
        pattern = "        U"
        templates = convert_to_hash_value_list(pattern)

        self.assertEquals(len(templates), 1)
        self.assertTrue(1 in templates)

    def test_convert_to_2(self):
        pattern = "        T"
        templates = convert_to_hash_value_list(pattern)

        self.assertEquals(len(templates), 1)
        self.assertTrue(2 in templates)

    def test_convert_to_3(self):
        pattern = "       U "
        templates = convert_to_hash_value_list(pattern)

        self.assertEquals(len(templates), 1)
        self.assertTrue(3 in templates)

    def test_convert_to_6(self):
        pattern = "       T "
        templates = convert_to_hash_value_list(pattern)

        self.assertEquals(len(templates), 1)
        self.assertTrue(6 in templates)
    

    def test_convert_8_spaces(self):
        pattern = "        "
        templates = convert_to_hash_value_list(pattern)

        print templates
        self.assertEquals(len(templates), 6) # 2 * 3 ** (9 - 8)

        self.assertTrue(0 in templates)
        self.assertTrue(1 in templates)
        self.assertTrue(2 in templates)
        # TODO: other end
        #self.assertTrue(0 in templates) # special case - duplicate
        self.assertTrue(6561 in templates)
        self.assertTrue((2 * 6561) in templates)

    # TODO: Test mirrors. We only need to create them if the pattern is assymetric

# Argh. I need to create MANY templates per pattern, with more for shorter patterns - beyond the length of the pattern is unknown

if __name__ == "__main__":
    unittest.main()



