#!/usr/bin/env python

import unittest
from nearby_filter import *
from board import *

import pdb

class NearbyFilterTest(unittest.TestCase):
    def test_start_in_the_middle_13(self):
        b = Board(13)
        f = NearbyFilter(b)
        l = list(f.get_iter())
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(6,6))

    def test_start_in_the_middle_9(self):
        b = Board(9)
        f = NearbyFilter(b)
        l = list(f.get_iter())
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0],(4,4))

    def test_enter_move(self):
        #pdb.set_trace()
        b = Board(9)
        f = NearbyFilter(b)
        f.move((2,2))
        l = list(f.get_iter())
        self.assertEquals(len(l), 16)
        #pdb.set_trace()
        # Inner circle:
        self.assertIn((1,2),l)
        self.assertIn((1,3),l)
        self.assertIn((2,3),l)
        self.assertIn((3,3),l)
        self.assertIn((3,2),l)
        self.assertIn((3,1),l)
        self.assertIn((2,1),l)
        self.assertIn((1,1),l)
        # Outer circle:
        self.assertIn((0,2),l)
        self.assertIn((0,4),l)
        self.assertIn((2,4),l)
        self.assertIn((4,4),l)
        self.assertIn((4,2),l)
        self.assertIn((4,0),l)
        self.assertIn((2,0),l)
        self.assertIn((0,0),l)

    def test_enter_2_moves(self):
        b = Board(9)
        f = NearbyFilter(b)
        f.move((2,2))
        f.move((3,2))
        actual = list(f.get_iter())
        expected = set()
        # Move 1
        # Inner circle:
        expected.add((1,2))
        expected.add((1,3))
        expected.add((2,3))
        expected.add((3,3))
        expected.add((3,2))
        expected.add((3,1))
        expected.add((2,1))
        expected.add((1,1))
        
        # Outer circle:
        expected.add((0,2))
        expected.add((0,4))
        expected.add((2,4))
        expected.add((4,4))
        expected.add((4,2))
        expected.add((4,0))
        expected.add((2,0))
        expected.add((0,0))
        # Move 2
        # Inner circle:
        expected.add((2,2))
        expected.add((2,3))
        expected.add((3,3))
        expected.add((4,3))
        expected.add((4,2))
        expected.add((4,1))
        expected.add((3,1))
        expected.add((2,1))
        # Outer circle:
        expected.add((1,2))
        expected.add((1,4))
        expected.add((3,4))
        expected.add((5,4))
        expected.add((5,2))
        expected.add((5,0))
        expected.add((3,0))
        expected.add((1,0))
        
        for pos in expected:
            self.assertIn(pos,actual)
            actual.remove(pos)
        self.assertEquals(len(actual), 0)

    def test_capture(self):
        b = Board(9)
        f = NearbyFilter(b)
        f.move((3,2)) # Move 1 - not used
        f.move((2,2)) # Move 2 - not used
        f.move((4,2)) # Move 3
        f.move((5,2)) # Move 4
        f.capture((3,2))
        f.capture((4,2))
        actual = list(f.get_iter())
        expected = set()

        # Capture 1: 3,2
        # pos
        expected.add((3,2))
        # Inner circle:
        expected.add((2,2))
        expected.add((2,3))
        expected.add((3,3))
        expected.add((4,3))
        expected.add((4,2))
        expected.add((4,1))
        expected.add((3,1))
        expected.add((2,1))
        
        # Capture 2: 4,2
        # pos
        expected.add((4,2))
        # Inner circle:
        expected.add((3,2))
        expected.add((3,3))
        expected.add((4,3))
        expected.add((5,3))
        expected.add((5,2))
        expected.add((5,1))
        expected.add((4,1))
        expected.add((3,1))

        # Move 3: 4,2
        # Inner circle:
        expected.add((3,2))
        expected.add((3,3))
        expected.add((4,3))
        expected.add((5,3))
        expected.add((5,2))
        expected.add((5,1))
        expected.add((4,1))
        expected.add((3,1))
        
        # Outer circle:
        expected.add((2,2))
        expected.add((2,4))
        expected.add((4,4))
        expected.add((6,4))
        expected.add((6,2))
        expected.add((6,0))
        expected.add((4,0))
        expected.add((2,0))

        # Move 4: 5,2
        # Inner circle:
        expected.add((4,2))
        expected.add((4,3))
        expected.add((5,3))
        expected.add((6,3))
        expected.add((6,2))
        expected.add((6,1))
        expected.add((5,1))
        expected.add((4,1))
        # Outer circle:
        expected.add((3,2))
        expected.add((3,4))
        expected.add((5,4))
        expected.add((7,4))
        expected.add((7,2))
        expected.add((7,0))
        expected.add((5,0))
        expected.add((3,0))
        
        for pos in expected:
            self.assertIn(pos,actual)
            actual.remove(pos)
        #self.assertEquals(len(actual), 0)

if __name__ == "__main__":
    unittest.main()

