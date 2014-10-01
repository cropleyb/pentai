#!/usr/bin/env python

import unittest

from pentai.base.defines import *
from pentai.base.pos import *

class PosTest(unittest.TestCase):

    def test_create(self):
        ds = Pos(8,5)

        self.assertEquals(ds[0], 8)
        self.assertEquals(ds[1], 5)
