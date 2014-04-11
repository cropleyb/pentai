#!/usr/bin/env python

import unittest

from pentai.base.bit_reverse import *

class BitReverseTest(unittest.TestCase):

    def test_reverse(self):
        x = reverse_mask(0xF3000000)
        self.assertEquals(x, 0x000000CF)

    def test_reverse_empty(self):
        x = reverse_mask(0x00000000)
        self.assertEquals(x, 0x00000000)

    def test_reverse_full(self):
        x = reverse_mask(0xFFFFFFFF)
        self.assertEquals(x, 0xFFFFFFFF)

    def test_reverse_covers_all(self):
        x = reverse_mask(0x33330000)
        self.assertEquals(x, 0x0000CCCC)

    ##############################
    # Now for 64 bits

    def test_reverse64(self):
        x = reverse_mask64(0xF300000000000000)
        self.assertEquals(x, 0x00000000000000CF)

    def test_reverse_empty64(self):
        x = reverse_mask64(0x0000000000000000)
        self.assertEquals(x, 0x0000000000000000)

    def test_reverse_full64(self):
        x = reverse_mask64(0xFFFFFFFFFFFFFFFF)
        self.assertEquals(x, 0xFFFFFFFFFFFFFFFF)

    def test_reverse_covers_all64(self):
        x = reverse_mask64(0x3333333300000000)
        self.assertEquals(x, 0x00000000CCCCCCCC)

    def test_reverse_doesnt_toggle_colours(self):
        x = reverse_mask64(0x55555555AAAAAAAA)
        self.assertEquals(x, 0xAAAAAAAA55555555)

if __name__ == "__main__":
    unittest.main()

