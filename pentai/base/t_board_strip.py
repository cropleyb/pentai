#!/usr/bin/env python

import unittest

from pentai.base.board_strip import *

class BoardStripTest(unittest.TestCase):
    def test_empty_board_strip_is_empty(self):
        bs = 0
        self.assertEquals(get_occ(bs, 0), EMPTY)

    def test_empty_board_strip_place_one_black_piece(self):
        bs = set_occ(0, 0, P1)
        self.assertEquals(get_occ(bs, 0), P1)

    def test_empty_board_strip_place_one_white_piece(self):
        bs = set_occ(0, 1, P2)
        self.assertEquals(get_occ(bs, 1), P2)

    def test_empty_board_strip__one_white_piece_far(self):
        bs = set_occ(0, 18, P2)
        self.assertEquals(get_occ(bs, 18), P2)

    def test_empty_board_strip_black_piece_far(self):
        bs = set_occ(0, 18, P1)
        self.assertEquals(get_occ(bs, 18), P1)

    def test_place_two_pieces(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P1)
        self.assertEquals(get_occ(bs, 1), P1)
        self.assertEquals(get_occ(bs, 2), P1)

    def test_place_two_pieces_widely(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 21, P2)
        self.assertEquals(get_occ(bs, 1), P1)
        self.assertEquals(get_occ(bs, 21), P2)
        self.assertEquals(get_occ(bs, 13), EMPTY)

    #####################################

class BoardStripCaptureTest(unittest.TestCase):
    def test_match_black_capture_left(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 7, P1) # Not involved in the capture
        self.assertEquals(match_capture_left(bs, 4, P1), (3,2))
        # 3 and 2 are the indices of the captured stones
        
    def test_dont_match_black_capture_left(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_capture_left(bs, 4, P1), ())

    def test_dont_match_black_capture_left_already_occupied(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_capture_left(bs, 4, P1), ())

    def test_dont_match_white_capture_left_already_occupied(self):
        bs = set_occ(0, 1, P2)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P2)
        self.assertEquals(match_capture_left(bs, 4, P2), ())

    def test_match_black_capture_mid_strip_left(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_capture_left(bs, 6, P1), (5,4))

    def test_dont_match_black_capture_left_mid_strip(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_capture_left(bs, 6, P1), ())

    def test_dont_match_black_capture_left_off_board(self):
        bs = set_occ(0, 0, P2)
        bs = set_occ(bs, 1, P2)
        self.assertEquals(match_capture_left(bs, 2, P1), ())

    #####################################

    def test_match_black_capture_right(self):
        bs = set_occ(0, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_capture_right(bs, 1, P1), (2,3))
        
    def test_dont_match_black_capture_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P1)
        self.assertEquals(match_capture_right(bs, 0, P1), ())

    def test_dont_match_black_capture_right_already_occupied(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_capture_right(bs, 1, P1), ())

    def test_dont_match_white_capture_right_already_occupied(self):
        bs = set_occ(0, 1, P2)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P2)
        self.assertEquals(match_capture_right(bs, 1, P2), ())

    def test_match_black_capture_mid_strip(self):
        bs = set_occ(0, 3, P2)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 5, P1)
        self.assertEquals(match_capture_right(bs, 2, P1), (3,4))

    def test_dont_match_black_capture_right_mid_strip(self):
        bs = set_occ(0, 3, P2)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, P1)
        self.assertEquals(match_capture_right(bs, 2, P1), ())

    #####################################

    def test_match_white_capture_right(self):
        bs = set_occ(0, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 8, P1) # Not involved in the capture
        self.assertEquals(match_capture_right(bs, 1, P2), (2,3))
        
    def test_dont_match_white_capture_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P2)
        self.assertEquals(match_capture_right(bs, 0, P2), ())

    def test_match_white_capture_mid_strip_right(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, P1)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_capture_right(bs, 2, P2), (3,4))

    def test_dont_match_white_capture_right_mid_strip(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_capture_right(bs, 2, P2), ())

    #####################################

class BoardStripThreatTest(unittest.TestCase):
    def test_match_black_threat_left(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 7, P1) # Not involved in the threat
        self.assertEquals(match_threat_left(bs, 4, P1), (3,2))
        
    def test_dont_match_black_threat_left(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_left(bs, 4, P1), ())

    def test_dont_match_black_threat_left_already_occupied(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_threat_left(bs, 4, P1), ())

    def test_dont_match_white_threat_left_already_occupied(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P2)
        self.assertEquals(match_threat_left(bs, 4, P2), ())

    def test_match_black_threat_mid_strip_left(self):
        bs = set_occ(0, 3, EMPTY)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_threat_left(bs, 6, P1), (5,4))

    def test_dont_match_black_threat_left_mid_strip(self):
        bs = set_occ(0, 3, EMPTY)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_threat_left(bs, 6, P1), ())

    def test_dont_match_black_threat_left_off_board(self):
        bs = set_occ(0, 0, P2)
        bs = set_occ(bs, 1, P2)
        self.assertEquals(match_threat_left(bs, 2, P1), ())

    #####################################

    def test_match_black_threat_right(self):
        bs = set_occ(0, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, P1), (2,3))
        
    def test_dont_match_black_threat_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_right(bs, 0, P1), ())

    def test_dont_match_black_threat_right_already_occupied(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, P1), ())

    def test_dont_match_white_threat_right_already_occupied(self):
        bs = set_occ(0, 1, P2)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, EMPTY)
        self.assertEquals(match_threat_right(bs, 1, P2), ())

    def test_match_black_threat_mid_strip_right(self):
        bs = set_occ(0, 3, P2)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, P1), (3,4))

    def test_dont_match_black_threat_right_mid_strip(self):
        bs = set_occ(0, 3, P2)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, P1), ())

    #####################################

    def test_match_white_threat_right(self):
        bs = set_occ(0, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 8, P1) # Not involved in the threat
        self.assertEquals(match_threat_right(bs, 1, P2), (2,3))
        
    def test_dont_match_white_threat_right(self):
        bs = set_occ(0, 1, EMPTY)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, EMPTY)
        self.assertEquals(match_threat_right(bs, 0, P2), ())

    def test_match_white_threat_mid_strip_right(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, P1)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, P2), (3,4))

    def test_dont_match_white_threat_right_mid_strip(self):
        bs = set_occ(0, 3, P1)
        bs = set_occ(bs, 4, EMPTY)
        bs = set_occ(bs, 5, EMPTY)
        self.assertEquals(match_threat_right(bs, 2, P2), ())

class BoardStrip2Test(unittest.TestCase):
    def test_dont_match_5_from_empty(self):
        bs = 0
        self.assertEquals(match_five_in_a_row(bs, 2, P1), False)

    def test_match_5_left(self):
        bs = set_occ(0, 1, P1)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P1)
        bs = set_occ(bs, 5, P1)
        self.assertEquals(match_five_in_a_row(bs, 5, P1), True)

    def test_dont_match_4_left(self):
        bs = set_occ(0, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P1)
        bs = set_occ(bs, 5, P1)
        self.assertEquals(match_five_in_a_row(bs, 5, P1), False)

    def test_match_5_right(self):
        bs = set_occ(0, 0, P1)
        bs = set_occ(bs, 1, P1)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_five_in_a_row(bs, 0, P1), True)

    def test_dont_match_5_right_with_gap(self):
        bs = set_occ(0, 0, P1)
        bs = set_occ(bs, 1, P1)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_five_in_a_row(bs, 0, P1), False)

    def test_match_5_in_middle(self):
        bs = set_occ(0, 0, P1)
        bs = set_occ(bs, 1, P1)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_five_in_a_row(bs, 2, P1), True)

    def test_match_5_white_in_middle(self):
        bs = set_occ(0, 0, P2)
        bs = set_occ(bs, 1, P2)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P2)
        self.assertEquals(match_five_in_a_row(bs, 2, P2), True)

    def test_dont_match_5_zebra_in_middle(self):
        bs = set_occ(0, 0, P1)
        bs = set_occ(bs, 1, P2)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P1)
        self.assertEquals(match_five_in_a_row(bs, 2, P1), False)


class BoardStripEnclosedFourTest(unittest.TestCase):
    def test_black_match_enclosed_four(self):
        bs = set_occ(0, 0, P2)
        bs = set_occ(bs, 1, P1)
        bs = set_occ(bs, 2, P1)
        bs = set_occ(bs, 3, P1)
        bs = set_occ(bs, 4, P1)
        bs = set_occ(bs, 5, P2)
        self.assertEquals(match_enclosed_four(bs, 0, P1), True)
        self.assertEquals(match_enclosed_four(bs, 1, P1), True)
        self.assertEquals(match_enclosed_four(bs, 2, P1), True)
        self.assertEquals(match_enclosed_four(bs, 3, P1), True)
        self.assertEquals(match_enclosed_four(bs, 4, P1), True)
        self.assertEquals(match_enclosed_four(bs, 5, P1), True)

    def test_white_match_enclosed_four(self):
        bs = set_occ(0, 0, P1)
        bs = set_occ(bs, 1, P2)
        bs = set_occ(bs, 2, P2)
        bs = set_occ(bs, 3, P2)
        bs = set_occ(bs, 4, P2)
        bs = set_occ(bs, 5, P1)
        self.assertEquals(match_enclosed_four(bs, 0, P2), True)
        self.assertEquals(match_enclosed_four(bs, 1, P2), True)
        self.assertEquals(match_enclosed_four(bs, 2, P2), True)
        self.assertEquals(match_enclosed_four(bs, 3, P2), True)
        self.assertEquals(match_enclosed_four(bs, 4, P2), True)
        self.assertEquals(match_enclosed_four(bs, 5, P2), True)

if __name__ == "__main__":
    unittest.main()

