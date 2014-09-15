import unittest

#from pentai.base.defines import *
from pentai.base.pos cimport *

class PosCTest(unittest.TestCase):

    def test_create(self):
        cdef Pos p
        p = Pos(8,5)
        p.set(4,7)

        self.assertEquals(p[0], 4)
        self.assertEquals(p[1], 7)
        self.assertEquals(p.val, 7*19 + 4)

    def test_equals(self):
        cdef Pos p
        p = Pos(8,5)

        self.assertEquals(p, (8,5))

    def test_not_equals(self):
        cdef Pos p
        p = Pos(8,5)

        self.assertNotEquals(p, (6,5))
