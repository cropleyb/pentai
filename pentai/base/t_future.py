#!/usr/bin/env python

import unittest

from pentai.base.future import *

class TestClass:
    def __init__(self, a1, a2, size):
        self.a1 = a1
        self.a2 = a2
        self.size = size

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

class FutureTest(unittest.TestCase):
    def test_getattr_expands_future(self):
        tc = Future("TestClass", "pentai.base.t_future", 1, 2, size=13)
        self.assertEquals(tc.__dict__["_instance"], None)

        self.assertEquals(tc.size, 13)
        self.assertEquals(tc.a1, 1)
        self.assertEquals(tc.a2, 2)

    def test_set_size_expands_future(self):
        tc = Future("TestClass", "pentai.base.t_future", 1, 2, size=13)
        self.assertEquals(tc.__dict__["_instance"], None)

        tc.set_size(19)
        self.assertEquals(tc.get_size(), 19)
        self.assertEquals(tc.a1, 1)
        self.assertEquals(tc.a2, 2)

if __name__ == "__main__":
    unittest.main()



