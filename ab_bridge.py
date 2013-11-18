#!/usr/bin/python

import board
import game_state
import alpha_beta
import search_order
import search_filter
import game
import gui
from pos import *
from board_strip import *

from length_counter import *

class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None):
        if parent == None:
            self.black_lines = LengthCounter()
            self.white_lines = LengthCounter()
            self.filter_iterator = None
        else:
            self.black_lines = LengthCounter(parent.black_lines) # TODO: clone method
            self.white_lines = LengthCounter(parent.white_lines)
            self.filter_iterator = parent.filter_iterator.clone()

    def get_black_line_counts(self):
        return self.black_lines

    def get_white_line_counts(self):
        return self.white_lines

    def get_iter(self):
        return self.filter_iterator

    def set_state(self, s):
        self.state = s
        self.board().add_observer(self)
        if self.filter_iterator is None:
            self.filter_iterator = search_filter.FilterIterator(self.board().get_size())
        # TODO: Remove us as an observer from previous self.state

    def to_move_colour(self):
        return self.state.to_move_colour()

    def to_move(self):
        player = self.state.to_move_player()
        return player

    def __repr__(self):
        return self.state.__repr__()

    def utility(self, player):
        if player.get_colour() == BLACK:
            return self.black_util()
        if player.get_colour() == WHITE:
            return -self.black_util()

    def black_util(self):
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
        #print "black: %s, white: %s, score: %s" % (bl, wl, score)
        return score

    def score(self):
        return self.utility(None)

    def board(self):
        return self.state.board

    def before_set_occ(self, pos, colour):
        self._set_or_reset_occ(pos, False)

    def after_set_occ(self, pos, colour):
        self._set_or_reset_occ(pos, True)
        # Reduce the move filtering
        self.filter_iterator.widen(pos)

    def _set_or_reset_occ(self, pos, add):
        # update substrips
        brd = self.board()
        for direction in DIRECTIONS[:4]:
            l = brd.get_positions_in_line_through_pos(pos, direction, 4)
            occs = [brd.get_occ(i) for i in l]
            process_substrips(occs, self.black_lines, self.white_lines, add)
        '''
        # TODO next - still got some bugs to fix
        for ds in brd.get_direction_strips():
            # TODO: Fetch this just once, share between before and after.
            occs = ds.get_occ_list(pos, brd.get_size())
            process_substrips(occs, self.black_lines, self.white_lines, add)
        '''

    def create_state(self, move_pos):
        ab_child = ABState(self)

        # clone the base level state object
        base_child = game_state.GameState(self.state.game, self.state)

        # connect the two (including move hook)
        ab_child.set_state(base_child)

        # make the move for the base (which updates ab_child)
        base_child.make_move(move_pos)

        return ab_child

    def terminal(self):
        return self.state.get_won_by() != game.EMPTY

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
            except game_state.IllegalMoveException:
                # Ignore these
                pass

    def terminal_test(self, state):
        return state.terminal()

