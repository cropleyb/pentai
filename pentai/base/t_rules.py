#!/usr/bin/env python

import unittest

from pentai.base.rules import *

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

    def test_move_is_too_close_13_tournament(self):
        r = Rules(13, "tournament")
        self.assertEquals(r.move_is_too_close((6,6)), True)
        self.assertEquals(r.move_is_too_close((4,4)), True)
        self.assertEquals(r.move_is_too_close((3,4)), False)
        self.assertEquals(r.move_is_too_close((4,3)), False)
        self.assertEquals(r.move_is_too_close((8,8)), True)
        self.assertEquals(r.move_is_too_close((8,9)), False)
        self.assertEquals(r.move_is_too_close((9,8)), False)

    def test_move_is_too_close_13_std(self):
        r = Rules(13, "standard")
        self.assertEquals(r.move_is_too_close((6,6)), False)
        self.assertEquals(r.move_is_too_close((4,4)), False)
        self.assertEquals(r.move_is_too_close((3,4)), False)
        self.assertEquals(r.move_is_too_close((4,3)), False)
        self.assertEquals(r.move_is_too_close((8,8)), False)
        self.assertEquals(r.move_is_too_close((8,9)), False)
        self.assertEquals(r.move_is_too_close((9,8)), False)

    def test_move_is_too_close_19_tournament(self):
        r = Rules(19, "tournament")
        self.assertEquals(r.move_is_too_close((7,7)), True)
        self.assertEquals(r.move_is_too_close((8,8)), True)
        self.assertEquals(r.move_is_too_close((9,9)), True)
        self.assertEquals(r.move_is_too_close((10,10)), True)
        self.assertEquals(r.move_is_too_close((11,11)), True)
        self.assertEquals(r.move_is_too_close((12,13)), False)
        self.assertEquals(r.move_is_too_close((13,12)), False)

    def test_move_is_too_close_19_std(self):
        r = Rules(19, "standard")
        self.assertEquals(r.move_is_too_close((10,10)), False)
        self.assertEquals(r.move_is_too_close((8,8)), False)
        self.assertEquals(r.move_is_too_close((7,8)), False)
        self.assertEquals(r.move_is_too_close((8,7)), False)
        self.assertEquals(r.move_is_too_close((12,12)), False)
        self.assertEquals(r.move_is_too_close((12,13)), False)
        self.assertEquals(r.move_is_too_close((13,12)), False)

    def test_tournament_move_not_ok(self):
        r = Rules(19, "tournament")
        centre_move = (9,9)
        self.assertEquals(r.ok_third_move(centre_move), False)

    def test_standard_move_ok(self):
        r = Rules(19, "standard")
        centre_move = (9,9)
        self.assertEquals(r.ok_third_move(centre_move), True)

    def test_tournament_move_ok(self):
        r = Rules(19, "tournament")
        outer_move = (6,6)
        self.assertEquals(r.ok_third_move(outer_move), True)

    def test_standard_move_not_ok(self):
        r = Rules(19, "standard")
        outer_move = (6,6)
        # Legal, but not really recommended
        self.assertEquals(r.ok_third_move(outer_move), False)

if __name__ == "__main__":
    unittest.main()



