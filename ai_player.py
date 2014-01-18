import ab_game
import alpha_beta
import openings_mover
import openings_book
import player as p_m
import utility_calculator as uc_m

from defines import *

import threading

class AIPlayer(p_m.Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, search_filter, *args, **vargs):
        p_m.Player.__init__(self, *args, **vargs)

        self.max_depth = 1
        self.search_filter = search_filter
        self.genome = None # temp hack
        self.openings_book = None
        self.openings_filt = None

        self.utility_calculator = uc_m.UtilityCalculator()

    def __eq__(self, other):
        return self.genome == other.genome

    def use_openings_book(self):
        return not self.openings_book is None

    def set_use_openings_book(self, openings_book):
        self.openings_book = openings_book

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth
    
    def get_utility_calculator(self):
        return self.utility_calculator

    def get_priority_filter(self):
        return self.search_filter

    def attach_to_game(self, base_game):
        self.ab_game = ab_game.ABGame(
            base_game, search_filter=self.search_filter,
            utility_calculator=self.utility_calculator)

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
        return "computer"

    def search_thread(self, gui):
        action = self.do_the_search()
        if action:
            gui.enqueue_action(action)
            gui.trig()

    def do_the_search(self):
        if self.use_openings_book():
            base_game = self.ab_game.base_game

            if self.openings_filt is None:
                # ie first run through
                self.openings_filt = openings_mover.OpeningsMover(
                        self.openings_book, base_game)

            move = self.openings_filt.get_a_good_move()
            if move:
                return move
            else:
                # min depth for turning off openings book
                turn = base_game.get_move_number()
                if turn > 7: # This is a complete guess
                    self.make_opening_move = False

        ab_game = self.ab_game

        # TODO: Don't reset if it is our move, we have "thinking
        # in opponents time" turned on, and our opponent is not a computer
        ab_game.reset_transposition_table()

        md = self.max_depth

        #print ab_game.current_state

        move, value = alpha_beta.alphabeta_search(ab_game.current_state,
                ab_game, max_depth=md)
        if self.ab_game.interrupted:
            return
        action = move[0]
        if value < -INFINITY / 1000:
            # No matter what we do, there is a forceable loss.
            # Just take the first move suggested by the search filter -
            # it will look better than the AB suggestion
            sf = ab_game.current_state.utility_stats.search_filter
            our_colour = ab_game.current_state.to_move_colour()
            action = sf.get_iter(our_colour).next()

        # TODO: Start thinking in opponents time thread here.

        # TODO: if we were thinking in the opponent's time, return nothing

        #print " => %s" % (action,)
        return action

    def rating_factor(self):
        return self.max_depth / 2.0

    def set_interrupted(self):
        self.ab_game.interrupted = True
