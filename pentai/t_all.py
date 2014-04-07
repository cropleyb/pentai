#!/usr/bin/python

import unittest
#import importlib

#import misc_db as m_m
import pentai.base.t_all as b_t
import pentai.ai.t_all as ai_t
import pentai.db.t_all as db_t

'''
def iam(m_str):
    """ import and add a pkg """
    global all_tests

    pkg = importlib.import_package(m_str)

    suite = unittest.defaultTestLoader.loadTestsFromPackage(pkg)
    all_tests.addTest(suite)
'''

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    all_tests.addTest(b_t.suite())
    all_tests.addTest(ai_t.suite())
    all_tests.addTest(db_t.suite())
    #iam("base")

    return all_tests

def main():
#    m_m.get_instance("test_")

    unittest.TextTestRunner().run(suite())
    
#    m_m.delete("test_")

if __name__ == "__main__":
    main()
