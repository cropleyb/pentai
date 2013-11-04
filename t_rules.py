#!/usr/bin/env python

import unittest
from rules import *

import pdb

class RulesTest(unittest.TestCase):
    #def setUp(self):

    '''
    def __init__(self, size, typeStr):
        self.size = size
        ts = typeStr.lower()
        if ts == "standard":
            self.centerFirst = True
            self.stonesForCaptureWin = 10
            self.canCapturePairs = True
            self.canCaptureThrees = False
            self.exactlyFive = False
    '''

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



