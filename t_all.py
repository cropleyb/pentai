#!/usr/bin/python

import unittest

import t_board
import t_length_counter
import t_alpha_beta
import t_ab_bridge
import t_rules
import t_text_gui
import t_game_state
import t_search_order
import t_utility
import t_ai_player

def suite():
    suite1 = unittest.defaultTestLoader.loadTestsFromModule(t_board)
    suite2 = unittest.defaultTestLoader.loadTestsFromModule(t_length_counter)
    suite3 = unittest.defaultTestLoader.loadTestsFromModule(t_alpha_beta)
    suite4 = unittest.defaultTestLoader.loadTestsFromModule(t_ab_bridge)
    suite5 = unittest.defaultTestLoader.loadTestsFromModule(t_rules)
    suite6 = unittest.defaultTestLoader.loadTestsFromModule(t_text_gui)
    suite7 = unittest.defaultTestLoader.loadTestsFromModule(t_game_state)
    suite8 = unittest.defaultTestLoader.loadTestsFromModule(t_search_order)
    suite9 = unittest.defaultTestLoader.loadTestsFromModule(t_utility)
    suite10 = unittest.defaultTestLoader.loadTestsFromModule(t_ai_player)
    allTests = unittest.TestSuite()
    allTests.addTest(suite1)
    allTests.addTest(suite2)
    allTests.addTest(suite3)
    allTests.addTest(suite4)
    allTests.addTest(suite5)
    allTests.addTest(suite6)
    allTests.addTest(suite7)
    allTests.addTest(suite8)
    allTests.addTest(suite9)
    allTests.addTest(suite10)
    return allTests

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
