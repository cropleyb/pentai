#!/usr/bin/python

import board
import game_state
import alpha_beta
import nearby_filter
import game
import gui
from board_strip import *

from length_counter import *

import pdb

CAPTURE_SCORE_BASE = 120 ** 3


class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None):
        if parent == None:
            self.black_lines = LengthCounter()
            self.white_lines = LengthCounter()
            self.search_filter = None
        else:
            self.black_lines = LengthCounter(parent.black_lines) # TODO: clone method
            self.white_lines = LengthCounter(parent.white_lines)
            self.search_filter = parent.search_filter.clone()

    def get_black_line_counts(self):
        return self.black_lines

    def get_white_line_counts(self):
        return self.white_lines

    def get_iter(self):
        return self.search_filter

    def set_state(self, s):
        self.state = s
        self.board().add_observer(self)
        if self.search_filter is None:
            self.search_filter = nearby_filter.NearbyFilter(self.board())
        # TODO: Remove us as an observer from previous self.state

    def to_move_colour(self):
        return self.state.to_move_colour()

    def to_move(self):
        player = self.state.to_move_player()
        return player

    def __repr__(self):
        ret = str(self.black_lines) + str(self.white_lines) + self.state.__repr__()
        return ret

    def search_player_colour(self):
        """ The AI player who is performing the search """
        game = self.game()
        return game.to_move_colour()

    def game(self):
        return self.state.game

    # TODO: Cache stuff somehow?
    def utility(self, search_player):
        #pdb.set_trace()
        search_colour = search_player.get_colour()
        turn_colour = self.to_move_colour()

        black_contrib = self.utility_contrib(self.black_lines, BLACK)
        white_contrib = self.utility_contrib(self.white_lines, WHITE)

        # Having the move is worth a lot.
        if turn_colour == BLACK:
            black_contrib *= 10
        else:
            white_contrib *= 10

        #print "B/W contrib: %s, %s, %s" % (black_contrib, white_contrib, self)
        if search_colour == BLACK:
            return black_contrib - white_contrib
        else:
            return white_contrib - black_contrib

    def utility_contrib(self, lines, colour):
        # Check for a win first
        # TODO: check rules
        captured = self.state.get_all_captured()
        if captured[colour] >= 10:
            return alpha_beta.infinity

        if lines[4] > 0:
            return alpha_beta.infinity

        # No win by "colour" found, fudge up a score
        score = 0

        for i in range(len(lines)):
            score *= 100
            rev = 4 - i
            score += lines[rev]

        cc = self.capture_contrib(captured[colour])
        score += cc
        # score += self.capture_contrib(captured[colour])
        #print "black: %s, white: %s, score: %s" % (self.black_lines, self.white_lines, \
        #        score)
        return score

    def capture_contrib(self, captures):
        """ captures become increasingly important as we approach 5 """
        # TODO: Use rules
        contrib = captures * CAPTURE_SCORE_BASE
        return contrib

    def score(self):
        return self.utility(None)

    def board(self):
        return self.state.board

    def before_set_occ(self, pos, colour):
        self._set_or_reset_occ(pos, False)

    def after_set_occ(self, pos, colour):
        self._set_or_reset_occ(pos, True)
        # Reduce the move filtering
        if colour == EMPTY:
            self.search_filter.capture(pos)
        else:
            self.search_filter.move(pos)

    def _set_or_reset_occ(self, pos, add):
        # update substrips
        brd = self.board()
        for ds in brd.get_direction_strips():
            # TODO: Fetch this just once, share between before and after.
            occs = ds.get_occ_list(pos, brd.get_size())
            #print "%s: %s" % (ds, occs)
            process_substrips(occs, self.black_lines, self.white_lines, add)

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

