from defines import *

import pdb

class NullFilter():
    """
    Don't do anything ;)
    """
    def __init__(self, orig=None, min_priority=0):
        pass

    def reset(self, orig=None, min_priority=0):
        pass

    def set_max_moves_func(self, mmf):
        pass

    def copy(self, min_priority=0):
        return self

    def get_iter(self, our_colour, depth=0, min_priority=0):
        """ This should not be called at all in production code. """
        #assert(False)
        if False:
            yield

    def __repr__(self):
        return "NullFilter"

    def add_or_remove_candidates(self, colour, length, pos_list, inc=1):
        pass

    def add_or_remove_take(self, colour, pos, inc=1):
        pass

    def add_or_remove_threat(self, colour, pos, inc=1):
        pass
