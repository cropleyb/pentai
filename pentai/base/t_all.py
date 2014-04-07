#!/usr/bin/python

import unittest
import importlib

def iam(m_str):
    """ import and add a module """
    global all_tests

    module = importlib.import_module("pentai.base.%s" % m_str)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    all_tests.addTest(suite)

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    iam("t_rules")
    iam("t_bit_reverse")
    iam("t_board_strip")
    iam("t_game_state")
    iam("t_board")
    iam("t_direction_strips")
    iam("t_game")

    return all_tests

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__":
    main()
