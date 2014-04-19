#!/usr/bin/env python

import unittest
import os

import misc_db as m_m
import zodb_dict as z_m
from pentai.base.defines import *

class MiscDBTest(unittest.TestCase):
    def setUp(self):
        self.misc_db = m_m.get_instance()

    def tearDown(self):
        pass

    def test_save_and_get_int(self):
        self.misc_db["whatever"] = 5
        z_m.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["whatever"], 5)

    def test_save_and_get_list_of_strings(self):
        self.misc_db["los"] = ["who", "am", "I"]
        z_m.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["los"], ["who", "am", "I"])


if __name__ == "__main__":
    unittest.main()

