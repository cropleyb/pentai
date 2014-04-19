#!/usr/bin/python

import unittest
import importlib
import os

import misc_db as m_m

def iam(m_str):
    """ import and add a module """
    global all_tests

    module = importlib.import_module("pentai.db.%s" % m_str)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    all_tests.addTest(suite)

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    iam("t_mru_cache")
    iam("t_misc_db")
    iam("t_games_mgr")
    iam("t_ai_factory")
    iam("t_preserved_game")
    iam("t_players_mgr")
    iam("t_openings_book")

    return all_tests

def main():
    st()

    m_m.get_instance("test_")
    z_m.set_db("test.db")

    unittest.TextTestRunner().run(suite())
    
    m_m.delete("test_")
    os.unlink("test.db")

if __name__ == "__main__":
    main()
