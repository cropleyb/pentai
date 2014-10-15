# Use this file to temporarily replace main.py, to run the PentAI
# unit test suite. Some kivy platforms (iOS) require the entry point to 
# be called main.py

import pentai.t_all as t_m
t_m.main()

'''
# Use this for detailed single case testing

import unittest
import pentai.base.t_board_strip as tmod

suite = unittest.TestSuite()
suite.addTest(tmod.BoardStripTest('test_empty_board_strip__one_white_piece_far'))
unittest.TextTestRunner().run(suite)
'''
