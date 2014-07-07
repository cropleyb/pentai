#!/usr/bin/env python

import unittest

from pentai.ai.choice_stats import *

""" Want:
Best value was at:
Depth v1  v2  v3  v4  v5  v6  v7  v8  v9
  1   40  30  20   5   5
    And:
Relative value to best:
Depth v1  v2  v3  v4  v5  v6  v7  v8  v9
  1   
"""

class ChoiceStatsTest(unittest.TestCase):
    def test_report_p1(self):
        cs = ChoiceStats()
        cs.report_vals(depth=2, save_values=[2,4,1,3,0])
        bva = cs.get_best_vals_at(depth=2)
        self.assertEquals(bva, [0,1,0,0,0])

    def test_report_p2(self):
        cs = ChoiceStats()
        cs.report_vals(depth=5, save_values=[4,1,-2,0,-1,7])
        bva = cs.get_best_vals_at(5)
        self.assertEquals(bva, [0,0,1,0,0,0])

    def test_report_p1_twice(self):
        cs = ChoiceStats()
        cs.report_vals(depth=2, save_values=[2,4,1,3,0])
        cs.report_vals(depth=2, save_values=[1,5,2,4,3])
        bva = cs.get_best_vals_at(depth=2)
        self.assertEquals(bva, [0,2,0,0,0])

    def test_report_p1_and_p2(self):
        cs = ChoiceStats()
        cs.report_vals(depth=2, save_values=[2,4,1,3,0])
        cs.report_vals(depth=3, save_values=[1,1,0,2,4,3])
        bva2 = cs.get_best_vals_at(depth=2)
        self.assertEquals(bva2, [0,1,0,0,0,0])
        bva3 = cs.get_best_vals_at(depth=3)
        self.assertEquals(bva3, [0,0,1,0,0,0])

    # TODO
    def test_rel_val_list(self):
        cs = ChoiceStats()
        cs.report_vals(depth=0, save_values=[1,2,3,4,3,2,0])
        rvl = cs.rel_val_list(depth=0)
        expected = (2.0 ** 1) / (2.0 ** 4)
        self.assertEquals(rvl, [expected])


    def test_first_val_is_best(self):
        cs = ChoiceStats()
        cs.report_vals(depth=4, save_values=[4,3,2,0])
        rvl = cs.rel_val_list(depth=4)
        self.assertEquals(rvl, [])

    def test_rel_val_list_two_entries(self):
        cs = ChoiceStats()
        cs.report_vals(depth=6, save_values=[2,4,5,3,2,0])
        cs.report_vals(depth=6, save_values=[1,4,2,0])
        rvl = cs.rel_val_list(depth=6)
        expected1 = (2.0 ** 2) / (2.0 ** 5)
        expected2 = (2.0 ** 1) / (2.0 ** 4)
        self.assertEquals(rvl, [expected1, expected2])

    # TODO: Neg vals.

    '''
    # TODO
    def test_report_safe_threshold(self):
        cs = ChoiceStats()
        cs.report_vals(depth=2, save_values=[2,4,1,3,0])
        cs.report_vals(depth=2, save_values=[1,2,3,2,2])
        s_t = cs.safe_threshold(depth=2, best=3)
        self.assertEquals(s_t, 1.0)
    '''

if __name__ == "__main__":
    unittest.main()
