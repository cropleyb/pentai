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
    def assert_almost_equals(self, l1, l2):
        self.assertEquals(len(l1), len(l2))
        for i, item1 in enumerate(l1):
            self.assertAlmostEquals(item1, l2[i])

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

    def test_rel_val_list(self):
        cs = ChoiceStats()
        cs.report_vals(depth=0, save_values=[1,2,3,4,3,2,0])
        rvl = cs.rel_val_list(depth=0)
        expected = (EXP_BASE ** 1) / (EXP_BASE ** 4)
        self.assertAlmostEquals(rvl, [expected])

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
        expected1 = (EXP_BASE ** 2) / (EXP_BASE ** 5)
        expected2 = (EXP_BASE ** 1) / (EXP_BASE ** 4)
        self.assert_almost_equals(rvl, [expected1, expected2])

    def test_rel_val_list_two_entries_for_p2(self):
        cs = ChoiceStats()
        cs.report_vals(depth=3, save_values=[2,4,1,3,2,3])
        cs.report_vals(depth=3, save_values=[1,4,2,0,2])
        rvl = cs.rel_val_list(depth=3)
        expected1 = (EXP_BASE ** 1) / (EXP_BASE ** 4)
        expected2 = (EXP_BASE ** 0) / (EXP_BASE ** 4)
        self.assert_almost_equals(rvl, [expected1, expected2])

    # TODO: Neg vals, big vals

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
