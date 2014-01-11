
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

# Forward and Reverse operations for an x, y pos, when applying
# the sequence of operations
def fwd0(x, y):
    return (x, y)

def rev0(x, y):
    return (x, y)

def fwd1(x, y):
    return (y, x)

def rev1(x, y):
    return (y, x)

def fwd2(x, y):
    return (y, -x)

def rev2(x, y):
    return (-y, x)

def fwd3(x, y):
    return (-x, y)

def rev3(x, y):
    return (-x, y)

def fwd4(x, y):
    return (-x, -y)

def rev4(x, y):
    return (-x, -y)

def fwd5(x, y):
    return (-y, -x)

def rev5(x, y):
    return (-y, -x)

def fwd6(x, y):
    return (-y, x)

def rev6(x, y):
    return (y, -x)

def fwd7(x, y):
    return (x, -y)

def rev7(x, y):
    return (x, -y)

operations = [(None,          fwd0, rev0),
              (diagonal_flip, fwd1, rev1),
              (calendar_flip, fwd2, rev2),
              (diagonal_flip, fwd3, rev3),
              (calendar_flip, fwd4, rev4),
              (diagonal_flip, fwd5, rev5),
              (calendar_flip, fwd6, rev6),
              (diagonal_flip, fwd7, rev7)]

def standardise(orig_state):
    state = GameState(orig_state.game, parent=orig_state)
    possibilities = []

    for operation, fwd, rev in operations:
        possibilities.append((state, fwd, rev))
        state = GameState(state.game, parent=state)
        if operation != None:
            operation(state)

    possibilities.append((state, fwd, rev))

    pb = [(p[0].board.strips[0].strips, p) for p in possibilities]

    s = min(pb)[1]
    return s
