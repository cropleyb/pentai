#!/usr/bin/env python

import unittest
import mock

import pdb

from length_counter import *

def pattern_string_to_int_list(occ_str):
    ret = []
    mapping = {
        " ": 0, # empty
        "B": 1, # Black
        "W": 2, # White
    }
    for occ in occ_str:
        occ_int = mapping[occ]
        ret.append(occ_int)
    return ret


class SubStripCountingTest(unittest.TestCase):
    def setUp(self):
        self.black_counter = LengthCounter()
        self.white_counter = LengthCounter()
        self.candidate_accumulator = mock.Mock()

    # Helper
    def process_substrips_for_str(self, ss_str):
        pattern = pattern_string_to_int_list(ss_str)
        ca = self.candidate_accumulator
        bc = self.black_counter
        wc = self.white_counter
        process_substrips(pattern, ca, bc, wc, True)

    # Tests
    def test_count_empty(self):
        self.process_substrips_for_str("         ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_single_black(self):
        self.process_substrips_for_str("    B    ")
        self.assertEquals(self.black_counter.tup(), (5,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_single_white(self):
        self.process_substrips_for_str("    W    ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (5,0,0,0,0))

    def test_count_single_black_at_end(self):
        self.process_substrips_for_str("B        ")
        self.assertEquals(self.black_counter.tup(), (1,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_open_three(self):
        self.process_substrips_for_str("   BBB   ")
        self.assertEquals(self.black_counter.tup(), (0,2,3,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_open_four(self):
        self.process_substrips_for_str("  BBBB   ")
        self.assertEquals(self.black_counter.tup(), (0,1,2,2,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_closed_four(self):
        self.process_substrips_for_str(" WBBBB   ")
        self.assertEquals(self.black_counter.tup(), (0,1,1,1,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_open_three_with_space_and_single_white(self):
        self.process_substrips_for_str(" W BBB   ")
        self.assertEquals(self.black_counter.tup(), (0,1,2,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_double_split_three(self):
        self.process_substrips_for_str("  B B B  ")
        self.assertEquals(self.black_counter.tup(), (0,4,1,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_split_four(self):
        self.process_substrips_for_str("  BBB B  ")
        self.assertEquals(self.black_counter.tup(), (0,1,3,1,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_middle_split_four(self):
        self.process_substrips_for_str("  BB BB  ")
        self.assertEquals(self.black_counter.tup(), (0,2,2,1,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_five_mid(self):
        self.process_substrips_for_str("  BBBBB  ")
        self.assertEquals(self.black_counter.tup(), (0,0,2,2,1))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_opponent_five(self):
        self.process_substrips_for_str("  WWWWW  ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,2,2,1))

    def test_count_five_side(self):
        self.process_substrips_for_str("BBBBB    ")
        self.assertEquals(self.black_counter.tup(), (1,1,1,1,1))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_five_side_with_stopper(self):
        self.process_substrips_for_str("BBBBBW   ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,1))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_count_three_side_with_stopper(self):
        self.process_substrips_for_str("BBB  W   ")
        self.assertEquals(self.black_counter.tup(), (0,0,1,0,0))
        self.assertEquals(self.white_counter.tup(), (2,0,0,0,0))

    def test_pre_threaten_pair(self):
        self.process_substrips_for_str("     WW  ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (1,3,0,0,0))

    def test_threaten_pair(self):
        self.process_substrips_for_str("    BWW  ")
        self.assertEquals(self.black_counter.tup(), (1,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_threaten_two_pairs(self):
        self.process_substrips_for_str("  WWBWW  ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_block_four(self):
        self.process_substrips_for_str("    BWWWW")
        self.assertEquals(self.black_counter.tup(), (1,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_too_short(self):
        self.process_substrips_for_str("W   ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_very_short(self):
        self.process_substrips_for_str("B")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (0,0,0,0,0))

    def test_diagonal_weirdness(self):
        self.process_substrips_for_str("  W  ")
        self.assertEquals(self.black_counter.tup(), (0,0,0,0,0))
        self.assertEquals(self.white_counter.tup(), (1,0,0,0,0))

class CandidateReportingTest(unittest.TestCase):
    def setUp(self):
        self.black_counter = LengthCounter()
        self.white_counter = LengthCounter()
        self.candidate_accumulator = mock.Mock()

    def process_substrips_for_str(self, ss_str):
        pattern = pattern_string_to_int_list(ss_str)
        ca = self.candidate_accumulator
        bc = self.black_counter
        wc = self.white_counter
        process_substrips(pattern, ca, bc, wc, True)

    def test_report_nothing(self):
        self.process_substrips_for_str("     ")
        calls = self.candidate_accumulator.mockGetAllCalls()
        self.assertEquals(len(calls),0)

    def test_report_a_four(self):
        #pdb.set_trace()
        self.process_substrips_for_str("BB BB")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 4, (2,))

    def test_report_a_different_four(self):
        self.process_substrips_for_str("B BBB")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 4, (1,))

    def test_report_a_three(self):
        self.process_substrips_for_str("B B B")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 3, (1,3,))

    def test_report_a_three_and_a_two(self):
        self.process_substrips_for_str("B B B ")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),2)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 3, (1,3,))
        ca.mockCheckCall(1, 'report_candidate', BLACK, 2, (1,3,5))

    def test_report_a_white_four(self):
        self.process_substrips_for_str("WW WW")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', WHITE, 4, (2,))

    def test_report_a_four(self):
        self.process_substrips_for_str(" WB BBB")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 4, (3,))

    def test_report_a_five(self):
        self.process_substrips_for_str(" WBBBBB")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),1)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 5, ())

    def test_report_two_ones(self):
        self.process_substrips_for_str(" W    ")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),2)
        ca.mockCheckCall(0, 'report_candidate', WHITE, 1, (0,2,3,4))
        ca.mockCheckCall(1, 'report_candidate', WHITE, 1, (2,3,4,5))

    def test_report_five_ones(self):
        #pdb.set_trace()
        self.process_substrips_for_str("    B    ")
        ca = self.candidate_accumulator
        calls = ca.mockGetAllCalls()
        self.assertEquals(len(calls),5)
        ca.mockCheckCall(0, 'report_candidate', BLACK, 1, (0,1,2,3))
        ca.mockCheckCall(1, 'report_candidate', BLACK, 1, (1,2,3,5))
        ca.mockCheckCall(2, 'report_candidate', BLACK, 1, (2,3,5,6))
        ca.mockCheckCall(3, 'report_candidate', BLACK, 1, (3,5,6,7))
        ca.mockCheckCall(4, 'report_candidate', BLACK, 1, (5,6,7,8))

if __name__ == "__main__":
    unittest.main()



