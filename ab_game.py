#!/usr/bin/python

import board
import pente_exceptions

from ab_state import *

class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, base_game, search_filter=None,
                 utility_calculator=None):
        s = self.current_state = ABState(None, search_filter, utility_calculator)
        s.set_state(base_game.current_state)
        self.base_game = base_game
        self.interrupted = False

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def utility(self, state):
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

    def terminal_test(self, state):
        if self.interrupted:
            return True
        return state.terminal()

