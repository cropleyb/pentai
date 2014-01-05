#!/usr/bin/env python

import unittest
from null_filter import *

import pdb

class NullFilterTest(unittest.TestCase):
    def setUp(self):
        self.nf = NullFilter()

    def arc(self, *args, **kwargs):
        self.nf.add_or_remove_candidates(*args, **kwargs)

    def test_get_iter_yields_nothing(self):
        l = list(self.nf.get_iter(BLACK))
        self.assertEquals(len(l), 0)


if __name__ == "__main__":
    unittest.main()

