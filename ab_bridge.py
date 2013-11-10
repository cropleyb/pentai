#!/usr/bin/python

import board
import game_state
import alpha_beta
import search_order
import game
import gui
from pos import *

from length_counter import *

import pdb

class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self):
        self.black_lines = LengthCounter()
        self.white_lines = LengthCounter()

    def set_state(self, s):
        self.state = s
        self.board().add_observer(self)
        # TODO: Remove us as an observer from previous self.state

    def to_move(self):
        return self.state.to_move()

    def __repr__(self):
        return self.state.__repr__()

    def utility(self, player):
        bl = self.black_lines
        wl = self.white_lines
        score = 0
        if bl[4] > 0:
            return alpha_beta.infinity
        if wl[4] > 0:
            return -alpha_beta.infinity
        # TODO: use an accessor
        # captures = self.state.captured

        # TODO: check rules, use captures

        for i in range(len(bl)):
            rev = 4 - i
            score += bl[rev]
            score -= wl[rev]
            score *= 100
        return score

    def score(self):
        return self.utility(None)

    def board(self):
        return self.state.board

    def before_set_occ(self, pos, colour):
        self.black_lines.set_add_mode(False)
        self.white_lines.set_add_mode(False)
        self._set_or_reset_occ(pos)

    def after_set_occ(self, pos, colour):
        self.black_lines.set_add_mode(True)
        self.white_lines.set_add_mode(True)
        self._set_or_reset_occ(pos)

    def _set_or_reset_occ(self, pos):
        # update substrips
        for direction in DIRECTIONS[:4]:
            l = self.board().get_positions_in_line_through_pos(pos, direction, 4)
            occs = [self.board().get_occ(i) for i in l]
            add_substrips(occs, self.black_lines, self.white_lines)

    def create_state(self, move_pos):
        ab_child = ABState()

        # clone the base level state object
        base_child = game_state.GameState(self.state.game, self.state)

        # connect the two (including move hook)
        ab_child.set_state(base_child)

        # make the move for the base (which updates ab_child)
        base_child.make_move(game.Move(move_pos))

        return ab_child

    def terminal(self):
        return self.state.get_won_by() != game.EMPTY

class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, base_game):
        s = self.current_state = ABState()
        s.set_state(base_game.current_state)
        self.base_game = base_game
        self.pos_iter = search_order.PosIterator(base_game.size())

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def make_move(self, x, y):
        self.current_state.set_colour(Pos(x,y), 1)

    def utility(self, state, player):
        return state.utility(player)

    def successors(self, state):
        for pos in self.pos_iter.get_iter():
            # create a AB_State for each possible move from state
            try:
                succ = state.create_state(pos)
                yield gui.MoveAction(game.Move(pos)), succ
            except game_state.IllegalMoveException:
                # Ignore these
                pass

    def terminal_test(self, state):
        return state.terminal()

