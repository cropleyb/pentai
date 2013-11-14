#!/usr/bin/env python

import unittest

import pdb

from board_strip import *

class BoardStripTest(unittest.TestCase):
    def test_empty_board_strip_is_empty(self):
        strip = BoardStrip()
        self.assertEquals(strip.get_occ(0), EMPTY)

    def test_empty_strip_place_one_black_piece(self):
        strip = BoardStrip()
        strip.set_occ(0, BLACK)
        self.assertEquals(strip.get_occ(0), BLACK)

    def test_empty_strip_place_one_white_piece(self):
        strip = BoardStrip()
        strip.set_occ(1, WHITE)
        self.assertEquals(strip.get_occ(1), WHITE)

    def test_empty_strip_place_one_white_piece_far(self):
        strip = BoardStrip()
        strip.set_occ(18, WHITE)
        self.assertEquals(strip.get_occ(18), WHITE)

    def test_empty_strip_place_one_black_piece_far(self):
        strip = BoardStrip()
        strip.set_occ(18, BLACK)
        self.assertEquals(strip.get_occ(18), BLACK)

    def test_place_two_pieces(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(2, BLACK)
        self.assertEquals(strip.get_occ(1), BLACK)
        self.assertEquals(strip.get_occ(2), BLACK)

    def test_place_two_pieces_widely(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(21, WHITE)
        self.assertEquals(strip.get_occ(1), BLACK)
        self.assertEquals(strip.get_occ(21), WHITE)
        self.assertEquals(strip.get_occ(13), EMPTY)

    #####################################

    def test_match_black_capture_left(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(2, WHITE)
        strip.set_occ(3, WHITE)
        strip.set_occ(7, BLACK) # Not involved in the capture
        self.assertEquals(strip.match_capture_left(4, BLACK), (3,2))
        
    def test_dont_match_black_capture_left(self):
        strip = BoardStrip()
        strip.set_occ(1, BLACK)
        strip.set_occ(2, WHITE)
        strip.set_occ(3, EMPTY)
        self.assertEquals(strip.match_capture_left(4, BLACK), ())

    def test_match_black_capture_mid_strip_left(self):
        strip = BoardStrip()
        strip.set_occ(3, BLACK)
        strip.set_occ(4, WHITE)
        strip.set_occ(5, WHITE)
        self.assertEquals(strip.match_capture_left(6, BLACK), (5,4))

    def test_dont_match_black_capture_left_mid_strip(self):
        strip = BoardStrip()
        strip.set_occ(3, BLACK)
        strip.set_occ(4, EMPTY)
        strip.set_occ(5, WHITE)
        self.assertEquals(strip.match_capture_left(6, BLACK), ())

    def test_dont_match_black_capture_left_off_board(self):
        strip = BoardStrip()
        strip.set_occ(0, WHITE)
        strip.set_occ(1, WHITE)
        self.assertEquals(strip.match_capture_left(2, BLACK), ())

    #####################################

    def test_match_black_capture_right(self):
        strip = BoardStrip()
        strip.set_occ(2, WHITE)
        strip.set_occ(3, WHITE)
        strip.set_occ(4, BLACK)
        self.assertEquals(strip.match_capture_right(1, BLACK), (2,3))
        
    def test_dont_match_black_capture_right(self):
        strip = BoardStrip()
        strip.set_occ(1, EMPTY)
        strip.set_occ(2, WHITE)
        strip.set_occ(3, BLACK)
        self.assertEquals(strip.match_capture_right(0, BLACK), ())

    def test_match_black_capture_mid_strip_right(self):
        strip = BoardStrip()
        strip.set_occ(3, WHITE)
        strip.set_occ(4, WHITE)
        strip.set_occ(5, BLACK)
        self.assertEquals(strip.match_capture_right(2, BLACK), (3,4))

    def test_dont_match_black_capture_right_mid_strip(self):
        strip = BoardStrip()
        strip.set_occ(3, WHITE)
        strip.set_occ(4, EMPTY)
        strip.set_occ(5, BLACK)
        self.assertEquals(strip.match_capture_right(2, BLACK), ())

    #####################################

    def test_match_white_capture_right(self):
        strip = BoardStrip()
        strip.set_occ(2, BLACK)
        strip.set_occ(3, BLACK)
        strip.set_occ(4, WHITE)
        strip.set_occ(8, BLACK) # Not involved in the capture
        self.assertEquals(strip.match_capture_right(1, WHITE), (2,3))
        
    def test_dont_match_white_capture_right(self):
        strip = BoardStrip()
        strip.set_occ(1, EMPTY)
        strip.set_occ(2, BLACK)
        strip.set_occ(3, WHITE)
        self.assertEquals(strip.match_capture_right(0, WHITE), ())

    def test_match_white_capture_mid_strip_right(self):
        strip = BoardStrip()
        strip.set_occ(3, BLACK)
        strip.set_occ(4, BLACK)
        strip.set_occ(5, WHITE)
        self.assertEquals(strip.match_capture_right(2, WHITE), (3,4))

    def test_dont_match_white_capture_right_mid_strip(self):
        strip = BoardStrip()
        strip.set_occ(3, BLACK)
        strip.set_occ(4, EMPTY)
        strip.set_occ(5, WHITE)
        self.assertEquals(strip.match_capture_right(2, WHITE), ())

if __name__ == "__main__":
    unittest.main()



