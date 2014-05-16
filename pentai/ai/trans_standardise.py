#!/usr/bin/env python

from pentai.base.game_state import *

def shift(orig_state):
    state = GameState(orig_state.game, parent=orig_state)
    brd = state.board
    east_occs = brd.d_strips[0].strips
    south_occs = brd.d_strips[2].strips

    board_size = brd.get_size()

    leftmost = rightmost = -1
    lowest = highest = -1

    #st()

    for i in range(board_size):
        if leftmost < 0 and south_occs[i] > 0:
            leftmost = i
        if lowest < 0 and east_occs[i] > 0:
            lowest = i
        if south_occs[i] > 0 and i > rightmost:
            rightmost = i
        if east_occs[i] > 0 and i > highest:
            highest = i

    l_shift = 0
    d_shift = 0

    # | . . . . . . .
    # | 0 1 2 3 4 5 6
    # Something at 5 (5,y) should stay there.
    # Something at 6 (6,y) should move to 5 (l_shift 1)

    # .  .  .  .  .  .  . |
    # 12 13 14 15 16 17 18
    # Something at 14 (14,y) should stay there.
    # Something at 13 or 12 (13,y) should move to 5 (d_shift 1)

    if leftmost >= 5 and rightmost < board_size - 5:
        l_shift = leftmost - 5
    if lowest >= 5 and highest < board_size - 5:
        d_shift = lowest - 5

    east_occs = east_occs[d_shift:]
    l_factor = 4 ** l_shift
    ret_e_occs = [o / l_factor for o in east_occs]
    brd.d_strips[0].strips = ret_e_occs
    
    return state, l_shift, d_shift
    
