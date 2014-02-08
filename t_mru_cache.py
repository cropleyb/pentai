#!/usr/bin/env python

import unittest

import mru_cache as m_m

class MiscDBTest(unittest.TestCase):
    def setUp(self):
        self.mruc = m_m.MRUCache(10)

    def test_save_and_get_str(self):
        self.mruc.add('x')
        top_5 = self.mruc.top(5)
        self.assertEquals(top_5, ['x'])

    def test_save_and_get_a_few(self):
        self.mruc.add(1)
        self.mruc.add(2)
        self.mruc.add(3)
        top_5 = self.mruc.top(5)
        self.assertEquals(top_5, [3,2,1])

    def test_save_more_than_cache_size(self):
        for i in range(1, 21):
            self.mruc.add(i)
        top_5 = self.mruc.top(5)
        self.assertEquals(top_5, [20,19,18,17,16])

    def test_add_duplicate(self):
        self.mruc.add(1)
        self.mruc.add(1)
        self.mruc.add(1)
        self.mruc.add(1)
        top_5 = self.mruc.top(5)
        self.assertEquals(top_5, [1])

    def test_add_something_again_goes_to_front(self):
        self.mruc.add(1)
        self.mruc.add(2)
        self.mruc.add(3)
        self.mruc.add(1)
        top_5 = self.mruc.top(5)
        self.assertEquals(top_5, [1,3,2])

    def test_request_more_than_cache_size(self):
        for i in range(1, 21):
            self.mruc.add(i)
        top_5 = self.mruc.top(20)
        self.assertEquals(top_5, [20,19,18,17,16,15,14,13,12,11])

if __name__ == "__main__":
    unittest.main()

