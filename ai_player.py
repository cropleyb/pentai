from pente_exceptions import *
import ab_game
import alpha_beta as ab_m
import openings_mover as om_m
import player as p_m
import utility_calculator as uc_m

from defines import *

import threading

skip_openings_book = False
def set_skip_openings_book(val):
    skip_openings_book = val

class AIPlayer(p_m.Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, search_filter, *args, **vargs):
        p_m.Player.__init__(self, *args, **vargs)

        self.max_depth = 1
        self.search_filter = search_filter
        self.genome = None # temp hack
        self.openings_book = None
        self.openings_mover = None

        self.utility_calculator = uc_m.UtilityCalculator()

    def __eq__(self, other):
        return self.genome == other.genome

    def use_openings_book(self):
        return not self.openings_book is None and not skip_openings_book

    def set_use_openings_book(self, openings_book):
        self.openings_book = openings_book

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth
    
    def get_utility_calculator(self):
        return self.utility_calculator

    def get_priority_filter(self):
        return self.search_filter

    def attach_to_game(self, base_game):
        self.ab_game = ab_game.ABGame(self, base_game)

    def prompt_for_action(self, base_game, gui, test=False):
        if test:
            return self.do_the_search()
        else:
            t = threading.Thread(target=self.search_thread, args=(gui,))

            # Allow the program to be exited quickly
            t.daemon = True

            t.start()
        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "Computer"

    def search_thread(self, gui):
        action = self.do_the_search()
        gui.enqueue_action(action)

    def get_openings_mover(self):
        if self.openings_mover is None:
            # ie first run through
            self.openings_mover = om_m.OpeningsMover(
                    self.openings_book, self.ab_game.base_game)
        return self.openings_mover

    def make_opening_move(self):
        if self.use_openings_book():
            base_game = self.ab_game.base_game

            om = self.get_openings_mover()
            move = om.get_a_good_move()
            if move:
                return move
            else:
                # min depth for turning off openings book
                turn = base_game.get_move_number()
                if turn > 15: # This is a complete guess
                    self.openings_book = None

    def do_the_search(self):
        try:
            return self.do_the_search_inner()
        except NoMovesException:
            self.ab_game.base_game.set_won_by(BLACK+WHITE)

    def do_the_search_inner(self):
        move = self.make_opening_move()
        if move:
            return move

        ab_game = self.ab_game

        # TODO: Don't reset if it is our move, we have "thinking
        # in opponents time" turned on, and our opponent is not a computer
        '''
        print "size of transposition table: %s" % len(ab_game.transposition_table)
        '''
        ab_game.reset_transposition_table()

        #print ab_game.current_state

        move, value = ab_m.alphabeta_search(ab_game.current_state, ab_game)
        if self.ab_game.interrupted:
            return
        action = move[0]

        # TODO: Start thinking in opponents time thread here.

        # TODO: if we were thinking in the opponent's time, return nothing

        #print " => %s" % (action,)
        return action

    def rating_factor(self):
        return max(self.max_depth-3, 0)

    def set_interrupted(self):
        self.ab_game.interrupted = True
