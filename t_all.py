#!/usr/bin/python

import unittest

import t_board
import t_length_lookup_table
import t_alpha_beta
import t_ab_state
import t_rules
import t_text_gui
import t_game_state
import t_search_order
import t_search_filter
import t_utility
import t_ai_player
import t_simpleton
import t_board_strip
import t_direction_strips
import t_nearby_filter
import t_take_counter
import t_threat_counter
import t_priority_filter
import t_priority_filter_2
import t_null_filter
import t_bit_reverse
import t_game
import t_blindness_filter
import t_openings_db
import t_standardise
import t_preserved_game
import t_ai_factory
import t_player_db
import t_game_manager

def add_module(m, all_tests):
    suite = unittest.defaultTestLoader.loadTestsFromModule(m)
    all_tests.addTest(suite)

def suite():
    all_tests = unittest.TestSuite()
    add_module(t_board, all_tests)
    add_module(t_length_lookup_table, all_tests)
    add_module(t_alpha_beta, all_tests)
    add_module(t_ab_state, all_tests)
    add_module(t_rules, all_tests)
    add_module(t_text_gui, all_tests)
    add_module(t_game_state, all_tests)
    add_module(t_search_order, all_tests)
    add_module(t_utility, all_tests)
    add_module(t_ai_player, all_tests)
    add_module(t_simpleton, all_tests)
    add_module(t_board_strip, all_tests)
    add_module(t_direction_strips, all_tests)
    add_module(t_search_filter, all_tests)
    add_module(t_nearby_filter, all_tests)
    add_module(t_take_counter, all_tests)
    add_module(t_priority_filter, all_tests)
    add_module(t_priority_filter_2, all_tests)
    add_module(t_null_filter, all_tests)
    add_module(t_threat_counter, all_tests)
    add_module(t_game, all_tests)
    add_module(t_bit_reverse, all_tests)
    add_module(t_blindness_filter, all_tests)
    add_module(t_openings_db, all_tests)
    add_module(t_standardise, all_tests)
    add_module(t_preserved_game, all_tests)
    add_module(t_ai_factory, all_tests)
    add_module(t_player_db, all_tests)
    add_module(t_game_manager, all_tests)

    return all_tests

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
