#!/usr/bin/python

import unittest

import pentai.base.t_all as b_t
import pentai.ai.t_all as ai_t
import pentai.gui.t_all as gui_t
import pentai.db.t_all as db_t
import pentai.db.zodb_dict as z_m
import pentai.db.test_db as tdb_m

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    all_tests.addTest(b_t.suite())
    all_tests.addTest(ai_t.suite())
    all_tests.addTest(db_t.suite())
    all_tests.addTest(gui_t.suite())

    return all_tests

def main():
    unittest.TextTestRunner().run(suite())

if __name__ == "__main__":
    main()
