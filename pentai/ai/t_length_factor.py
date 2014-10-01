#!/usr/bin/env python

import unittest

from pentai.ai.length_factor import *
from pentai.base.defines import *

class LengthFactorTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_factor(self):
        lf = LengthFactor()
        lf.set_default_factor(20)

        weight1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(weight1, 1)

        weight2 = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(weight2, 20)

    def test_different_default_factor(self):
        lf = LengthFactor()
        lf.set_default_factor(30)

        weight2 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(weight2, 900)

    def test_max_default_factor(self):
        lf = LengthFactor()
        lf.set_default_factor(2)

        weight = lf.get_weight(length=5, sub_type=0)
        self.assertEquals(weight, 16)

    def test_length_boost(self):
        lf = LengthFactor()
        lf.set_default_factor(2)
        #st()
        lf.set_length_boost(length=3, boost=3)

        weights = lf.get_weights()
        self.assertEquals(weights, [1,1,1,2,2,2,12,12,12,24,24,24,48,48,48])
        
        w1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(w1, 1)
        w2 = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(w2, 2)
        w3 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(w3, 12)
        w4 = lf.get_weight(length=4, sub_type=0)
        self.assertEquals(w4, 24)

    def test_2_length_boosts(self):
        lf = LengthFactor()
        lf.set_default_factor(2)
        lf.set_length_boost(length=2, boost=3)
        lf.set_length_boost(length=4, boost=5)

        w1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(w1, 1)
        w2 = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(w2, 6)
        w3 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(w3, 12)
        w4 = lf.get_weight(length=4, sub_type=0)
        self.assertEquals(w4, 120)

    def test_sub_type_0_boost(self):
        lf = LengthFactor()
        lf.set_default_factor(4)
        lf.set_sub_type_boost(length=2, sub_type=0, boost=3)

        w1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(w1, 1)
        w2a = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(w2a, 12)
        w2b = lf.get_weight(length=2, sub_type=1)
        self.assertEquals(w2b, 4)
        w2c = lf.get_weight(length=2, sub_type=2)
        self.assertEquals(w2c, 4)
        w3 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(w3, 16)
        w4 = lf.get_weight(length=4, sub_type=0)
        self.assertEquals(w4, 64)

    def test_sub_type_1_boost(self):
        lf = LengthFactor()
        lf.set_default_factor(4)
        lf.set_sub_type_boost(length=2, sub_type=1, boost=3)

        w1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(w1, 1)
        w2a = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(w2a, 4)
        w2b = lf.get_weight(length=2, sub_type=1)
        self.assertEquals(w2b, 12)
        w2c = lf.get_weight(length=2, sub_type=2)
        self.assertEquals(w2c, 4)
        w3 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(w3, 16)
        w4 = lf.get_weight(length=4, sub_type=0)
        self.assertEquals(w4, 64)

    def test_sub_type_2_boost(self):
        lf = LengthFactor()
        lf.set_default_factor(4)
        lf.set_sub_type_boost(length=2, sub_type=2, boost=3)

        w1 = lf.get_weight(length=1, sub_type=0)
        self.assertEquals(w1, 1)
        w2a = lf.get_weight(length=2, sub_type=0)
        self.assertEquals(w2a, 4)
        w2b = lf.get_weight(length=2, sub_type=1)
        self.assertEquals(w2b, 4)
        w2c = lf.get_weight(length=2, sub_type=2)
        self.assertEquals(w2c, 12)
        w3 = lf.get_weight(length=3, sub_type=0)
        self.assertEquals(w3, 16)
        w4 = lf.get_weight(length=4, sub_type=0)
        self.assertEquals(w4, 64)

if __name__ == "__main__":
    unittest.main()

