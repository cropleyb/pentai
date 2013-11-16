#!/usr/bin/env python

import unittest

from direction_strips import *
from pos import *

class DirectionStripsTest(unittest.TestCase):

    # East
    def test_e_create_direction_strips(self):
        ds = EDirectionStrips(board_size = 13)
    
    def test_e_unset_is_empty(self):
        ds = EDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ(Pos(1,5)), EMPTY)

    def test_e_set_and_get_black(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), BLACK)
        self.assertEquals(ds.get_occ(Pos(0,0)), BLACK)
    
    def test_e_set_and_get_white(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), WHITE)
        self.assertEquals(ds.get_occ(Pos(0,0)), WHITE)

    def test_e_capture(self):
        ds = EDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), BLACK)
        ds.set_occ(Pos(1,0), WHITE)
        ds.set_occ(Pos(2,0), WHITE)
        captures = ds.get_captures(Pos(3,0), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,0),(1,0)])
    
    #########################################
    # South East
    def test_se_create_direction_strips(self):
        ds = SEDirectionStrips(board_size = 13)
    
    def test_se_unset_is_empty(self):
        ds = SEDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ(Pos(1,5)), EMPTY)

    def test_se_set_and_get_black(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), BLACK)
        self.assertEquals(ds.get_occ(Pos(0,0)), BLACK)
    
    def test_se_set_and_get_white(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), WHITE)
        self.assertEquals(ds.get_occ(Pos(0,0)), WHITE)

    def test_se_capture(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,4), BLACK)
        ds.set_occ(Pos(1,3), WHITE)
        ds.set_occ(Pos(2,2), WHITE)
        captures = ds.get_captures(Pos(3,1), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,2),(1,3)])

    def test_another_se_capture(self):
        ds = SEDirectionStrips(board_size = 9)
        ds.set_occ(Pos(2,4), BLACK)
        ds.set_occ(Pos(3,3), WHITE)
        ds.set_occ(Pos(4,2), WHITE)
        captures = ds.get_captures(Pos(5,1), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(4,2),(3,3)])

    #########################################
    # South
    def test_s_create_direction_strips(self):
        ds = SDirectionStrips(board_size = 13)
    
    def test_s_unset_is_empty(self):
        ds = SDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ(Pos(1,5)), EMPTY)

    def test_s_set_and_get_black(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), BLACK)
        self.assertEquals(ds.get_occ(Pos(0,0)), BLACK)
    
    def test_s_set_and_get_white(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), WHITE)
        self.assertEquals(ds.get_occ(Pos(0,0)), WHITE)

    def test_s_capture(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,4), BLACK)
        ds.set_occ(Pos(0,3), WHITE)
        ds.set_occ(Pos(0,2), WHITE)
        captures = ds.get_captures(Pos(0,1), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(0,2),(0,3)])

    def test_another_s_capture(self):
        ds = SDirectionStrips(board_size = 9)
        ds.set_occ(Pos(2,6), BLACK)
        ds.set_occ(Pos(2,5), WHITE)
        ds.set_occ(Pos(2,4), WHITE)
        captures = ds.get_captures(Pos(2,3), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,4),(2,5)])
    

    #########################################
    # South West
    def test_sw_create_direction_strips(self):
        ds = SWDirectionStrips(board_size = 13)
    
    def test_sw_unset_is_empty(self):
        ds = SWDirectionStrips(board_size = 9)
        self.assertEquals(ds.get_occ(Pos(1,5)), EMPTY)

    def test_sw_set_and_get_black(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), BLACK)
        self.assertEquals(ds.get_occ(Pos(0,0)), BLACK)
    
    def test_sw_set_and_get_white(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ(Pos(0,0), WHITE)
        self.assertEquals(ds.get_occ(Pos(0,0)), WHITE)

    def test_sw_capture(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ(Pos(4,4), BLACK)
        ds.set_occ(Pos(3,3), WHITE)
        ds.set_occ(Pos(2,2), WHITE)
        captures = ds.get_captures(Pos(1,1), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,2),(3,3)])

    def test_another_sw_capture(self):
        ds = SWDirectionStrips(board_size = 9)
        ds.set_occ(Pos(4,6), BLACK)
        ds.set_occ(Pos(3,5), WHITE)
        ds.set_occ(Pos(2,4), WHITE)
        captures = ds.get_captures(Pos(1,3), BLACK)
        self.assertEquals(len(captures),2)
        self.assertEquals(captures,[(2,4),(3,5)])
    
    #########################################
    '''
    #########################################
    # pos in line through pos for substrips #
    #########################################
    def test_get_positions_in_E_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (1,0), 4)
        self.assertEquals(piltp,
                [(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7)])

    def test_get_positions_in_SE_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (1,1), 4)
        self.assertEquals(piltp,
                [(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11)])

    def test_get_positions_in_S_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (0,1), 4)
        self.assertEquals(piltp,
                [(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11)])

    def test_get_positions_in_SW_line_through_pos(self):
        board = Board(size = 13)
        piltp = board.get_positions_in_line_through_pos(Pos(7,7), (-1,1), 4)
        self.assertEquals(piltp,
                [(11,3),(10,4),(9,5),(8,6),(7,7),(6,8),(5,9),(4,10),(3,11)])
    '''


if __name__ == "__main__":
    unittest.main()



