#!/usr/bin/python

import board
import pente_exceptions
import gui # TODO

from ab_state import *

CAPTURE_SCORE_BASE = 120 ** 3

class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, base_game):
        s = self.current_state = ABState()
        s.set_state(base_game.current_state)
        self.base_game = base_game

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def utility(self, state, player):
        return state.utility(player)

    # TODO: unit test
    def successors(self, state):
        pos_iter = state.get_iter()
        for pos in pos_iter.get_iter():
            # create a AB_State for each possible move from state
            try:
                succ = state.create_state(pos)
                yield gui.MoveAction(pos), succ
            except pente_exceptions.IllegalMoveException:
                # Ignore these
                pass

    def terminal_test(self, state):
        return state.terminal()

