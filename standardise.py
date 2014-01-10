
from bit_reverse import *

from game_state import *

import pdb

""" N.B. These 3 operations only process the horizontal and vertical
representations of the board, so the diagonal representations will be
broken and unusable for further moves and utility calculations
"""

def bit_pair_reverse(brd, strips):
    for i in range(len(strips)):
        occs = strips[i]
        new_occs = reverse_mask64(occs)
        # We only use the first (board size * 2) bits
        new_occs >>= (32 - brd.get_size() << 1)
        strips[i] = new_occs

def list_reverse(strips):
    strips.reverse()

def page_flip(state):
    brd = state.get_board()
    east_occs = brd.strips[0]
    south_occs = brd.strips[2]

    bit_pair_reverse(brd, east_occs.strips)
    list_reverse(south_occs.strips)

    return state
    
def calendar_flip(state):
    brd = state.get_board()
    east_occs = brd.strips[0]
    south_occs = brd.strips[2]

    list_reverse(east_occs.strips)
    bit_pair_reverse(brd, south_occs.strips)

    return state

def diagonal_flip(state):
    brd = state.get_board()
    east_occs = brd.strips[0].strips
    south_occs = brd.strips[2].strips
    brd.strips[0].strips = south_occs
    brd.strips[2].strips = east_occs
    return state

def standardise(orig_state):
    state = orig_state
    possibilities = []

    for operation in [diagonal_flip, calendar_flip,
                      diagonal_flip, calendar_flip,
                      diagonal_flip, calendar_flip,
                      diagonal_flip]:
        state = GameState(state.game, parent=state)
        possibilities.append(state)
        operation(state)

    possibilities.append(state)

    pb = [(p.board.strips[0].strips, p) for p in possibilities]

    s = min(pb)[1]
    return s
