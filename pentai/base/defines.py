INFINITY = 1e+31

DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
               (0,-1),        (0,1),
               (1,-1), (1,0), (1,1))

EMPTY = 0
BLACK = 1
WHITE = 2

def opposite_colour(col):
    if col == BLACK:
        return WHITE
    elif col == WHITE:
        return BLACK
    return EMPTY

from pdb import set_trace as st

import logger as log
'''
def print_func():
    pass
    #print sys._getframe(1).f_code.co_name
'''
