#!/usr/bin/env python

from pentai.base.game_state import *

def shift(orig_state):
    state = GameState(orig_state.game, parent=orig_state)
    #e_strips = state.board.d_strips[0].strips
    brd = state.board
    east_occs = brd.d_strips[0].strips
    south_occs = brd.d_strips[2].strips

    board_size = brd.get_size()

    leftmost = rightmost = 0
    lowest = highest = 0

    for i in range(board_size):
        if leftmost == 0 and south_occs[i] > 0:
            leftmost = i
        if lowest == 0 and east_occs[i] > 0:
            lowest = i
        if south_occs[i] > rightmost:
            rightmost = i
        if east_occs[i] > highest:
            highest = i

    l_shift = 0
    d_shift = 0

    if leftmost > 5 and rightmost < board_size - 4:
        l_shift = leftmost - 6
    if lowest > 5 and highest < board_size - 4:
        d_shift = lowest - 6

    east_occs = east_occs[d_shift:]
    l_factor = 4 ** l_shift
    ret_e_occs = [o / l_factor for o in east_occs]
    brd.d_strips[0].strips = ret_e_occs
    
    return state, l_shift, d_shift
    

