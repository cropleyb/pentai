INFINITY = 1e+31

DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
               (0,-1),        (0,1),
               (1,-1), (1,0), (1,1))

EMPTY = 0
P1 = 1
P2 = 2

def opposite_colour(col):
    if col == P1:
        return P2
    elif col == P2:
        return P1
    return EMPTY

from pdb import set_trace as st

'''
def print_func():
    pass
    #print sys._getframe(1).f_code.co_name
'''
