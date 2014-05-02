from pentai.base.bit_reverse import *
from pentai.base.game_state import *

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
    east_occs = brd.d_strips[0]
    south_occs = brd.d_strips[2]

    bit_pair_reverse(brd, east_occs.strips)
    list_reverse(south_occs.strips)

    return state
    
def calendar_flip(state):
    brd = state.get_board()
    east_occs = brd.d_strips[0]
    south_occs = brd.d_strips[2]

    list_reverse(east_occs.strips)
    bit_pair_reverse(brd, south_occs.strips)

    return state

def diagonal_flip(state):
    brd = state.get_board()
    east_occs = brd.d_strips[0].strips
    south_occs = brd.d_strips[2].strips
    brd.d_strips[0].strips = south_occs
    brd.d_strips[2].strips = east_occs
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

operations = None
last_size = 0

def get_operation(ind, size):
    global operations, last_size

    if operations == None or last_size != size:
        def wrap(func):
            def w(x, y):
                xx, yy = func(x, y)
                if xx < 0:
                    xx += (size-1)
                if yy < 0:
                    yy += (size-1)
                return xx, yy
            return w
        operations = [(diagonal_flip, wrap(fwd1), wrap(rev1)),
                      (calendar_flip, wrap(fwd2), wrap(rev2)),
                      (diagonal_flip, wrap(fwd3), wrap(rev3)),
                      (calendar_flip, wrap(fwd4), wrap(rev4)),
                      (diagonal_flip, wrap(fwd5), wrap(rev5)),
                      (calendar_flip, wrap(fwd6), wrap(rev6)),
                      (diagonal_flip, wrap(fwd7), wrap(rev7))]
        last_size = size
    try:
        return operations[ind]
    except IndexError:
        pass

def standardise(orig_state):
    state = GameState(orig_state.game, parent=orig_state)
    possibilities = [(state, fwd0, rev0)]

    size = state.game.size()

    for ind in range(7):
        operation, fwd, rev = get_operation(ind, size)
        state = GameState(state.game, parent=state)
        operation(state)
        possibilities.append((state, fwd, rev))

    #st()
    pb = [(p[0].board.d_strips[0].strips, p) for p in possibilities]

    s = min(pb)[1]
    return s
