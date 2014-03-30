#!/usr/bin/env python

import unittest

from board_strip import *

class BoardStripTest(unittest.TestCase):
    def test_empty_board_strip_is_empty(self):
        bs = 0
        self.assertEquals(get_occ(bs, 0), EMPTY)

    def test_empty_board_strip_place_one_black_piece(self):
        bs = set_occ(0, 0, BLACK)
        self.assertEquals(get_occ(bs, 0), BLACK)

    def test_empty_board_strip_place_one_white_piece(self):
        bs = set_occ(0, 1, WHITE)
        self.assertEquals(get_occ(bs, 1), WHITE)

    def test_empty_board_strip__one_white_piece_far(self):
        bs = set_occ(0, 18, WHITE)
        self.assertEquals(get_occ(bs, 18), WHITE)

    def test_empty_board_strip_black_piece_far(self):
        bs = set_occ(0, 18, BLACK)
        self.assertEquals(get_occ(bs, 18), BLACK)

    def test_place_two_pieces(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        self.assertEquals(get_occ(bs, 1), BLACK)
        self.assertEquals(get_occ(bs, 2), BLACK)

    def test_place_two_pieces_widely(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 21, WHITE)
        self.assertEquals(get_occ(bs, 1), BLACK)
        self.assertEquals(get_occ(bs, 21), WHITE)
        self.assertEquals(get_occ(bs, 13), EMPTY)

    #####################################

class BoardStripCaptureTest(unittest.TestCase):
    def test_match_black_capture_left(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 7, BLACK) # Not involved in the capture
        self.assertEquals(match_capture_left(bs, 4, BLACK), (3,2))
        # 3 and 2 are the indices of the captured stones
        
    def test_dont_match_black_capture_left(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_capture_left(bs, 4, BLACK), ())

    def test_dont_match_black_capture_left_already_occupied(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_capture_left(bs, 4, BLACK), ())

    def test_dont_match_white_capture_left_already_occupied(self):
        bs = set_occ(0, 1, WHITE)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, WHITE)
        self.assertEquals(match_capture_left(bs, 4, WHITE), ())

    def test_match_black_capture_mid_strip_left(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_capture_left(bs, 6, BLACK), (5,4))

    def test_dont_match_black_capture_left_mid_strip(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_capture_left(bs, 6, BLACK), ())

    def test_dont_match_black_capture_left_off_board(self):
        bs = set_occ(0, 0, WHITE)
        bs = set_occ(bs, 1, WHITE)
        self.assertEquals(match_capture_left(bs, 2, BLACK), ())

    #####################################

    def test_match_black_capture_right(self):
        bs = set_occ(0, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_capture_right(bs, 1, BLACK), (2,3))
        
    def test_dont_match_black_capture_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, BLACK)
        self.assertEquals(match_capture_right(bs, 0, BLACK), ())

    def test_dont_match_black_capture_right_already_occupied(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_capture_right(bs, 1, BLACK), ())

    def test_dont_match_white_capture_right_already_occupied(self):
        bs = set_occ(0, 1, WHITE)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, WHITE)
        self.assertEquals(match_capture_right(bs, 1, WHITE), ())

    def test_match_black_capture_mid_strip(self):
        bs = set_occ(0, 3, WHITE)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 5, BLACK)
        self.assertEquals(match_capture_right(bs, 2, BLACK), (3,4))

    def test_dont_match_black_capture_right_mid_strip(self):
        bs = set_occ(0, 3, WHITE)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, BLACK)
        self.assertEquals(match_capture_right(bs, 2, BLACK), ())

    #####################################

    def test_match_white_capture_right(self):
        bs = set_occ(0, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 8, BLACK) # Not involved in the capture
        self.assertEquals(match_capture_right(bs, 1, WHITE), (2,3))
        
    def test_dont_match_white_capture_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, WHITE)
        self.assertEquals(match_capture_right(bs, 0, WHITE), ())

    def test_match_white_capture_mid_strip_right(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_capture_right(bs, 2, WHITE), (3,4))

    def test_dont_match_white_capture_right_mid_strip(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_capture_right(bs, 2, WHITE), ())

    #####################################

class BoardStripThreatTest(unittest.TestCase):
    def test_match_black_threat_left(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 7, BLACK) # Not involved in the threat
        self.assertEquals(match_threat_left(bs, 4, BLACK), (3,2))
        
    def test_dont_match_black_threat_left(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_left(bs, 4, BLACK), ())

    def test_dont_match_black_threat_left_already_occupied(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_threat_left(bs, 4, BLACK), ())

    def test_dont_match_white_threat_left_already_occupied(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, WHITE)
        self.assertEquals(match_threat_left(bs, 4, WHITE), ())

    def test_match_black_threat_mid_strip_left(self):
        bs = set_occ(0, 3, EMPTY)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_threat_left(bs, 6, BLACK), (5,4))

    def test_dont_match_black_threat_left_mid_strip(self):
        bs = set_occ(0, 3, EMPTY)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_threat_left(bs, 6, BLACK), ())

    def test_dont_match_black_threat_left_off_board(self):
        bs = set_occ(0, 0, WHITE)
        bs = set_occ(bs, 1, WHITE)
        self.assertEquals(match_threat_left(bs, 2, BLACK), ())

    #####################################

    def test_match_black_threat_right(self):
        bs = set_occ(0, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, BLACK), (2,3))
        
    def test_dont_match_black_threat_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_right(bs, 0, BLACK), ())

    def test_dont_match_black_threat_right_already_occupied(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, BLACK), ())

    def test_dont_match_white_threat_right_already_occupied(self):
        bs = set_occ(0, 1, WHITE)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, WHITE), ())

    def test_match_black_threat_mid_strip_right(self):
        bs = set_occ(0, 3, WHITE)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, BLACK), (3,4))

    def test_dont_match_black_threat_right_mid_strip(self):
        bs = set_occ(0, 3, WHITE)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, BLACK), ())

    #####################################

    def test_match_white_threat_right(self):
        bs = set_occ(0, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 8, BLACK) # Not involved in the threat
        self.assertEquals(match_threat_right(bs, 1, WHITE), (2,3))
        
    def test_dont_match_white_threat_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_right(bs, 0, WHITE), ())

    def test_match_white_threat_mid_strip_right(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, WHITE), (3,4))

    def test_dont_match_white_threat_right_mid_strip(self):
        bs = set_occ(0, 3, BLACK)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, WHITE), ())

class BoardStrip2Test(unittest.TestCase):
    def test_dont_match_5_from_empty(self):
        bs = 0
        self.assertEquals(match_five_in_a_row(bs, 2, BLACK), False)

    def test_match_5_left(self):
        bs = set_occ(0, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        bs = set_occ(bs, 5, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 5, BLACK), True)

    def test_dont_match_4_left(self):
        bs = set_occ(0, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        bs = set_occ(bs, 5, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 5, BLACK), False)

    def test_match_5_right(self):
        bs = set_occ(0, 0, BLACK)
        bs = set_occ(bs, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 0, BLACK), True)

    def test_dont_match_5_right_with_gap(self):
        bs = set_occ(0, 0, BLACK)
        bs = set_occ(bs, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 0, BLACK), False)

    def test_match_5_in_middle(self):
        bs = set_occ(0, 0, BLACK)
        bs = set_occ(bs, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 2, BLACK), True)

    def test_match_5_white_in_middle(self):
        bs = set_occ(0, 0, WHITE)
        bs = set_occ(bs, 1, WHITE)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, WHITE)
        self.assertEquals(match_five_in_a_row(bs, 2, WHITE), True)

    def test_dont_match_5_zebra_in_middle(self):
        bs = set_occ(0, 0, BLACK)
        bs = set_occ(bs, 1, WHITE)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, BLACK)
        self.assertEquals(match_five_in_a_row(bs, 2, BLACK), False)


class BoardStripEnclosedFourTest(unittest.TestCase):
    def test_black_match_enclosed_four(self):
        bs = set_occ(0, 0, WHITE)
        bs = set_occ(bs, 1, BLACK)
        bs = set_occ(bs, 2, BLACK)
        bs = set_occ(bs, 3, BLACK)
        bs = set_occ(bs, 4, BLACK)
        bs = set_occ(bs, 5, WHITE)
        self.assertEquals(match_enclosed_four(bs, 0, BLACK), True)
        self.assertEquals(match_enclosed_four(bs, 1, BLACK), True)
        self.assertEquals(match_enclosed_four(bs, 2, BLACK), True)
        self.assertEquals(match_enclosed_four(bs, 3, BLACK), True)
        self.assertEquals(match_enclosed_four(bs, 4, BLACK), True)
        self.assertEquals(match_enclosed_four(bs, 5, BLACK), True)

    def test_white_match_enclosed_four(self):
        bs = set_occ(0, 0, BLACK)
        bs = set_occ(bs, 1, WHITE)
        bs = set_occ(bs, 2, WHITE)
        bs = set_occ(bs, 3, WHITE)
        bs = set_occ(bs, 4, WHITE)
        bs = set_occ(bs, 5, BLACK)
        self.assertEquals(match_enclosed_four(bs, 0, WHITE), True)
        self.assertEquals(match_enclosed_four(bs, 1, WHITE), True)
        self.assertEquals(match_enclosed_four(bs, 2, WHITE), True)
        self.assertEquals(match_enclosed_four(bs, 3, WHITE), True)
        self.assertEquals(match_enclosed_four(bs, 4, WHITE), True)
        self.assertEquals(match_enclosed_four(bs, 5, WHITE), True)

if __name__ == "__main__":
    unittest.main()

