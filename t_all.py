#!/usr/bin/python

import unittest
import t_board
import t_update_substrips
import t_alpha_beta

def suite():
    suite1 = unittest.defaultTestLoader.loadTestsFromModule(t_board)
    suite2 = unittest.defaultTestLoader.loadTestsFromModule(t_update_substrips)
    suite3 = unittest.defaultTestLoader.loadTestsFromModule(t_alpha_beta)
    allTests = unittest.TestSuite()
    allTests.addTest(suite1)
    allTests.addTest(suite2)
    allTests.addTest(suite3)
    return allTests

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
