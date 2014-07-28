#!/usr/bin/python

import pentai.ai.ab_state as ab_s_m
from pentai.base.pente_exceptions import *
from pentai.base.defines import *

#import history_heuristic as hh_m
import pentai.ai.killer_heuristic as kh_m
import time

import pentai.ai.choice_stats as cs_m

choice_stats = cs_m.ChoiceStats()

class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, player, base_game):
        search_filter = player.search_filter
        '''
        if genome.utility_filter:
            search_filter.set_game(self)
        '''
        utility_calculator = player.utility_calculator
        self.max_depth = player.max_depth
        self.force_depth = player.force_depth
        self.bl_cutoff = player.bl_cutoff
        # Another failed experiment or two...
        #self.heuristic_stats = hh_m.HistoryHeuristicStats()
        self.heuristic_stats = kh_m.KillerHeuristicStats()
        try:
            #print "ABGame setting heuristic to self.heuristic_stats %s" % \
            #        self.heuristic_stats
            search_filter.set_heuristic(self.heuristic_stats)
        except AttributeError, e:
            #print e
            pass

        s = self.current_state = ab_s_m.ABState(None, search_filter, utility_calculator)
        s.set_state(base_game.current_state)
        self.base_game = base_game
        self.transposition_table = {} # TODO: extract class?
        #self.transposition_hits = 0
        self.sleep_count = 0

    def get_base_game(self):
        return self.base_game

    def get_rules(self):
        return self.base_game.get_rules()

    def get_move_number(self):
        return self.base_game.get_move_number()

    def get_last_move(self):
        return self.base_game.get_last_move()

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def reset_transposition_table(self):
        self.transposition_table = {}

    def reset_heuristic(self):
        self.heuristic_stats.reset()

    def report_short_circuit(self, move, depth):
        self.heuristic_stats.report_short_circuit(move, depth)

    def report_vals(self, depth, save_values):
        choice_stats.report_vals(depth, save_values)

    def use_bl_cutoff(self):
        return self.bl_cutoff

    def utility(self, state, depth):
        if depth >= 3:
            try:
                ret = state.cached_value
                return ret
            except AttributeError:
                pass

        self.sleep_count += 1
        if not self.sleep_count % 16:
            # Give other thread(s) some time too
            time.sleep(0.000001)

        return state.utility()

    # TODO: Where does this belong?
    def successors(self, state, depth):
            mn = state.get_move_number()
            tried_count = 0
            # This while loop is to make sure there is at least one move
            # suggested. The move number is to stop infinite loops when
            # there is a draw.
            while tried_count == 0 and mn < 70:
                # TODO: First move constraints are associated with the rules
                if mn == 1:
                    # The first P1 move is always in the centre
                    brd_size = self.base_game.get_board().get_size()
                    centre_pos = (brd_size/2, brd_size/2)
                    p_i = [centre_pos]
                else:
                    pos_iter = state.get_iter(state.to_move())
                    min_priority = 0
                    if depth > self.max_depth:
                        min_priority = 3
                        if depth % 2:
                            min_priority = 5
                    p_i = pos_iter.get_iter(state.to_move_colour(), state,
                            depth, min_priority, tried=state.get_seen())
                for pos in p_i:
                    # create an ABState for each possible move from state
                    try:
                        succ = state.create_state(pos)
                        tried_count += 1
                        yield pos, succ

                        if succ.terminal():
                            return
                    except IllegalMoveException:
                        pass

    def save_utility(self, state, depth, utility_value):
        """ Save to transposition table """
        if depth < 3:
            return
        key = state.board().key()
        self.transposition_table[key] = utility_value
        state.clean_up()

    def was_interrupted(self):
        return not self.base_game.is_live()

    def terminal_test(self, state, depth):
        if self.was_interrupted():
            return True
        # Check if we have this position in the transposition table
        try:
            key = state.board().key()
            val = self.transposition_table[key]
            # Yes, save it for returning from utility()
            state.cached_value = val
            #self.transposition_hits += 1
            # And return this node as terminal
            return True
        except KeyError:
            pass
        if depth >= (self.max_depth + self.force_depth):
            return True
        return state.terminal()

