#!/usr/bin/python

import pentai.ai.ab_state as ab_s_m
from pentai.base.pente_exceptions import *

class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, player, base_game):
        search_filter = player.search_filter
        utility_calculator = player.utility_calculator
        self.max_depth = player.max_depth
        self.force_depth = player.force_depth

        s = self.current_state = ab_s_m.ABState(None, search_filter, utility_calculator)
        s.set_state(base_game.current_state)
        self.base_game = base_game
        self.interrupted = False
        self.transposition_table = {} # TODO: extract class?
        #self.transposition_hits = 0

    def get_rules(self):
        return self.base_game.get_rules()

    def get_move_number(self):
        return self.base_game.get_move_number()

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def reset_transposition_table(self):
        self.transposition_table = {}

    def utility(self, state, depth):
        if depth >= 3:
            try:
                ret = state.cached_value
                return ret
            except AttributeError:
                pass

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
                    # The first black move is always in the centre
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
                    p_i = pos_iter.get_iter(state.to_move_colour(),
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

    def terminal_test(self, state, depth):
        if self.interrupted:
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

