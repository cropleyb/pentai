#!/usr/bin/python

import ab_state as ab_m


class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, base_game, search_filter=None,
                 utility_calculator=None):
        s = self.current_state = ab_m.ABState(None, search_filter, utility_calculator)
        s.set_state(base_game.current_state)
        self.base_game = base_game
        self.interrupted = False
        self.transposition_table = {} # TODO: extract class?
        #self.transposition_hits = 0

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
        # TODO: First move constraints are associated with the rules
        if mn == 1:
            # The first black move is always in the centre
            brd_size = self.base_game.get_board().get_size()
            centre_pos = (brd_size/2, brd_size/2)
            p_i = [centre_pos]
        else:
            pos_iter = state.get_iter(state.to_move())
            p_i = pos_iter.get_iter(state.to_move_colour(), depth=depth)
        tried_count = 0
        for pos in p_i:
            # create an ABState for each possible move from state
            succ = state.create_state(pos)
            yield pos, succ

            # Are we are at the top level of the search
            # and have we found a win (for ourselves)
            # This is just to finish games off quickly
            if self.current_state.terminal():
                return

    def save_utility(self, state, depth, utility_value):
        """ Save to transposition table """
        if depth < 3:
            return
        key = state.board().key()
        self.transposition_table[key] = utility_value

    def terminal_test(self, state):
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
        return state.terminal()

