#from pentai.base.pos cimport *

cdef board_width_type MAX_BOARD_WIDTH=19

cdef class Pos:
    def __cinit__(self):
        pass

    def __init__(self, *args):
        self.set(*args)

    def __getitem__(self, int i):
        if i:
            return self.val / MAX_BOARD_WIDTH
        else:
            return self.val % MAX_BOARD_WIDTH

    def set(self, *args):
        cdef board_width_type x, y
        x, y = args
        self.val = y * MAX_BOARD_WIDTH + x

    def _richcmp(self, other, compare_type):
        v1 = self.val
        v2 = other.val
        if compare_type == 2:
            return v1 == v2
        elif compare_type == 3:
            return v1 != v2
        elif compare_type == 0:
            return v1 < v2
        elif compare_type == 1:
            return v1 <= v2
        elif compare_type == 4:
            return v1 > v2
        elif compare_type == 5:
            return v1 >= v2

    def __richcmp__(self, other, compare_type):
        try:
            return self._richcmp(other, compare_type)
        except:
            x, y = other
            p2 = Pos(x, y)
            return self._richcmp(p2, compare_type)
