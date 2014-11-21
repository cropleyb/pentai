#!/usr/bin/env python

import unittest

from pentai.base.defines import *
from pentai.base.pos import *

class PosTest(unittest.TestCase):

    def test_create(self):
        ds = Pos(8,5)

        self.assertEquals(ds[0], 8)
        self.assertEquals(ds[1], 5)

    def test_set_params(self):
        ds = Pos()
        ds.set(3,4)

        self.assertEquals(ds[0], 3)
        self.assertEquals(ds[1], 4)

    def test_set_tuple(self):
        ds = Pos()
        ds.set((4,5))

        self.assertEquals(ds[0], 4)
        self.assertEquals(ds[1], 5)

    def test_compare(self):
        ds = Pos(1,2)

        self.assertEquals(ds, Pos(1,2))
        self.assertNotEquals(ds, Pos(1,3))
        self.assertNotEquals(ds, Pos(2,2))
        self.assertNotEquals(ds, Pos(2,1))
        self.assertLess(ds, Pos(2,2))
        self.assertLessEqual(ds, Pos(1,2))
        self.assertLessEqual(ds, Pos(2,2))
        self.assertGreater(ds, Pos(0,2))
        self.assertGreaterEqual(ds, Pos(1,2))
        self.assertGreaterEqual(ds, Pos(1,0))

    def test_compare_with_tuple(self):
        ds = Pos(1,2)

        self.assertGreaterEqual(ds, (1,0))

    def test_compare_with_list(self):
        ds = Pos(1,2)

        self.assertEqual(ds, [1,2])

    def test_compare_large_corner(self):
        self.assertGreaterEqual(Pos(18,18), Pos(18,17))
        self.assertGreaterEqual(Pos(18,18), Pos(17,18))
