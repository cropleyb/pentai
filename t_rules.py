#!/usr/bin/env python

import unittest
from rules import *

class RulesTest(unittest.TestCase):

    def test_board_size_13(self):
        r = Rules(13, "standard")
        self.assertEquals(r.size, 13)

    def test_board_size_19(self):
        r = Rules(19, "standard")
        self.assertEquals(r.size, 19)

    def test_board_size_9(self):
        r = Rules(9, "standard")
        self.assertEquals(r.size, 9)
        
    def test_board_size_20_throws(self):
        with self.assertRaises(BoardTooBigException):
            r = Rules(20, "standard")

    def test_board_size_4_throws(self):
        with self.assertRaises(BoardTooSmallException):
            r = Rules(4, "standard")


if __name__ == "__main__":
    unittest.main()



