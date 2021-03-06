#!/usr/bin/env python

import unittest

from pentai.base.defines import *
from pentai.base.direction_strips import *

class DirectionStripsTest(unittest.TestCase):

    # East
    def test_e_create_direction_strips(self):
        ds = EDirectionStrips(board_size = 13)
    
    def test_e_unset_is_empty(self):
        ds = EDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ((1,5)), EMPTY)

    def test_e_set_and_get_black(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P1)
        self.assertEquals(ds.get_occ((0,0)), P1)
    
    def test_e_set_and_get_white(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P2)
        self.assertEquals(ds.get_occ((0,0)), P2)

    def test_e_capture(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P1)
        ds.set_occ((1,0), P2)
        ds.set_occ((2,0), P2)
        captures = ds.get_captures((3,0), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,0),(1,0)])
    
    #########################################
    # South East
    def test_se_create_direction_strips(self):
        ds = SEDirectionStrips(board_size = 13)
    
    def test_se_unset_is_empty(self):
        ds = SEDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ((1,5)), EMPTY)

    def test_se_set_and_get_black(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P1)
        self.assertEquals(ds.get_occ((0,0)), P1)
    
    def test_se_set_and_get_white(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P2)
        self.assertEquals(ds.get_occ((0,0)), P2)

    def test_se_capture(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((0,4), P1)
        ds.set_occ((1,3), P2)
        ds.set_occ((2,2), P2)
        captures = ds.get_captures((3,1), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,2),(1,3)])

    def test_another_se_capture(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((2,4), P1)
        ds.set_occ((3,3), P2)
        ds.set_occ((4,2), P2)
        captures = ds.get_captures((5,1), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(4,2),(3,3)])

    #########################################
    # South
    def test_s_create_direction_strips(self):
        ds = SDirectionStrips(board_size = 13)
    
    def test_s_unset_is_empty(self):
        ds = SDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ((1,5)), EMPTY)

    def test_s_set_and_get_black(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P1)
        self.assertEquals(ds.get_occ((0,0)), P1)
    
    def test_s_set_and_get_white(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P2)
        self.assertEquals(ds.get_occ((0,0)), P2)

    def test_s_capture(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((0,4), P1)
        ds.set_occ((0,3), P2)
        ds.set_occ((0,2), P2)
        captures = ds.get_captures((0,1), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(0,2),(0,3)])

    def test_another_s_capture(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((2,6), P1)
        ds.set_occ((2,5), P2)
        ds.set_occ((2,4), P2)
        captures = ds.get_captures((2,3), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,4),(2,5)])
    

    #########################################
    # South West
    def test_sw_create_direction_strips(self):
        ds = SWDirectionStrips(board_size = 13)
    
    def test_sw_unset_is_empty(self):
        ds = SWDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ((1,5)), EMPTY)

    def test_sw_set_and_get_black(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P1)
        self.assertEquals(ds.get_occ((0,0)), P1)
    
    def test_sw_set_and_get_white(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P2)
        self.assertEquals(ds.get_occ((0,0)), P2)

    def test_sw_capture(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((4,4), P1)
        ds.set_occ((3,3), P2)
        ds.set_occ((2,2), P2)
        captures = ds.get_captures((1,1), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,2),(3,3)])

    def test_another_sw_capture(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((4,6), P1)
        ds.set_occ((3,5), P2)
        ds.set_occ((2,4), P2)
        captures = ds.get_captures((1,3), P1)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,4),(3,5)])
    
    ###############################################
    # pos in line through pos for length counters #
    ###############################################
    def test_empty_positions_in_E_line_through_pos(self):
        ds = SWDirectionStrips(board_size = 9)
        occ_list = ds.get_occ_list((3,4), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_position_in_E_line_through_pos(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((2,4), P2)
        occ_list = ds.get_occ_list((3,4), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, EMPTY, P2, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_E_line_through_pos(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((0,4), P2)
        occ_list = ds.get_occ_list((1,4), board_size=9)
        self.assertEquals(occ_list, \
                [P2, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_E_line_through_pos_b(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ((1,4), P2)
        occ_list = ds.get_occ_list((0,4), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, P2, EMPTY, EMPTY, EMPTY])

    #########

    def test_one_occ_position_in_SE_line_through_pos(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((2,4), P1)
        occ_list = ds.get_occ_list((3,3), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, EMPTY, P1, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_SE_line_through_pos(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((0,4), P2)
        occ_list = ds.get_occ_list((1,3), board_size=9)
        self.assertEquals(occ_list, \
                [P2, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_SE_line_through_pos_b(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ((1,3), P2)
        occ_list = ds.get_occ_list((0,4), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, P2, EMPTY, EMPTY, EMPTY])

    #########

    def test_one_occ_position_in_S_line_through_pos(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((2,4), P1)
        occ_list = ds.get_occ_list((2,3), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, EMPTY, EMPTY, EMPTY, P1, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_S_line_through_pos(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((4,0), P2)
        occ_list = ds.get_occ_list((4,1), board_size=9)
        self.assertEquals(occ_list, \
                [P2, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_S_line_through_pos_b(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ((4,1), P2)
        occ_list = ds.get_occ_list((4,0), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, P2, EMPTY, EMPTY, EMPTY])

    #########

    def test_one_occ_position_in_SW_line_through_pos(self):
        ds = SWDirectionStrips(board_size=5)
        ds.set_occ((2,4), P1)
        occ_list = ds.get_occ_list((1,3), board_size=5)
        self.assertEquals(occ_list, \
                [EMPTY, EMPTY, P1])

    def test_one_occ_border_position_in_SW_line_through_pos(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((0,0), P2)
        occ_list = ds.get_occ_list((1,1), board_size=9)
        self.assertEquals(occ_list, \
                [P2, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY])

    def test_one_occ_border_position_in_SW_line_through_pos_b(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ((1,1), P2)
        occ_list = ds.get_occ_list((0,0), board_size=9)
        self.assertEquals(occ_list, \
                [EMPTY, P2, EMPTY, EMPTY, EMPTY])

if __name__ == "__main__":
    unittest.main()



