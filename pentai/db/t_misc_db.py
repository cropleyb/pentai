#!/usr/bin/env python

import unittest

import misc_db as m_m
import os
from pentai.base.defines import *

class MiscDBTest(unittest.TestCase):
    def setUp(self):
        self.test_misc_fn = "test_misc.pkl"
        self.misc_db = m_m.MiscDB("test_")

    def tearDown(self):
        try:
            os.unlink(self.test_misc_fn)
        except OSError: pass

    def test_save_and_get_int(self):
        self.misc_db["whatever"] = 5
        self.misc_db.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["whatever"], 5)

    def test_save_and_get_list_of_strings(self):
        self.misc_db["los"] = ["who", "am", "I"]
        self.misc_db.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["los"], ["who", "am", "I"])


if __name__ == "__main__":
    unittest.main()

