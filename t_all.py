#!/usr/bin/python

import unittest

import importlib

def iam(m_str):
    """ import and add a module """
    global all_tests

    module = importlib.import_module(m_str)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    all_tests.addTest(suite)

def suite():
    global all_tests
    all_tests = unittest.TestSuite()
    iam("t_board")
    iam("t_length_lookup_table")
    iam("t_alpha_beta")
    iam("t_ab_state")
    iam("t_rules")
    iam("t_text_gui")
    iam("t_game_state")
    iam("t_utility")
    iam("t_ai_player")
    iam("t_board_strip")
    iam("t_direction_strips")
    iam("t_take_counter")
    iam("t_priority_filter")
    iam("t_priority_filter_2")
    iam("t_null_filter")
    iam("t_threat_counter")
    iam("t_game")
    iam("t_bit_reverse")
    iam("t_vision_filter")
    iam("t_openings_book")
    iam("t_standardise")
    iam("t_preserved_game")
    iam("t_ai_genome")
    iam("t_ai_factory")
    iam("t_players_mgr")
    iam("t_games_mgr")
    iam("t_openings_mover")
    iam("t_misc_db")
    iam("t_mru_cache")

    return all_tests

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
