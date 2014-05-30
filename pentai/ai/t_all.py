#!/usr/bin/python

import unittest
import importlib

def iam(m_str):
    """ import and add a module """
    global all_tests

    module = importlib.import_module("pentai.ai.%s" % m_str)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    all_tests.addTest(suite)

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    iam("t_alpha_beta")
    iam("t_ab_state")
    iam("t_length_lookup_table")
    iam("t_utility")
    iam("t_ai_player")
    iam("t_take_counter")
    iam("t_threat_counter")
    iam("t_priority_filter")
    iam("t_priority_filter_2")
    iam("t_priority_filter_3")
    iam("t_ai_genome")
    iam("t_rot_standardise")
    iam("t_trans_standardise")
    iam("t_standardise")
    iam("t_openings_mover")

    return all_tests

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__":
    main()
