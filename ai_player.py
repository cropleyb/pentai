import ab_game
import alpha_beta
from gui import *

from player import *
from priority_filter import *
from utility_calculator import *

import threading

class AIPlayer(Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, mmpdl, narrowing, *args, **vargs):
        Player.__init__(self, *args, **vargs)
        self.max_depth = 1

        self.search_filter = PriorityFilter()
        self.set_max_moves_per_depth_level(mmpdl, narrowing)

        self.utility_calculator = UtilityCalculator()

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth
    
    def set_max_moves_per_depth_level(self, mmpdl, narrowing):
        if narrowing != 0:
            def mmpdl_func(depth):
                return mmpdl - round(narrowing * depth)
        else:
            def mmpdl_func(depth):
                return mmpdl
        self.search_filter.set_max_moves_func(mmpdl_func)

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
        gui.enqueue_action(action)
        gui.trig()

    def do_the_search(self):
        ab_game = self.ab_game
        md = self.max_depth
        '''
        if ab_game.current_state.get_move_number() < 10:
            md = min(md, 4)
        '''
        # TODO: Move these to ABState.__repr__
        print ab_game.current_state

        move, value = alpha_beta.alphabeta_search(ab_game.current_state,
                ab_game, max_depth=md)
        action = move[0]
        if value < -INFINITY / 1000:
            # No matter what we do, there is a forceable loss.
            # Just take the first move suggested by the search filter -
            # it will look better than the AB suggestion
            pf = ab_game.current_state.utility_stats.search_filter
            our_colour = ab_game.current_state.to_move_colour()
            action = pf.get_iter(our_colour).next()

        #print " => %s" % (action,)
        return action

    def set_interrupted(self):
        self.ab_game.interrupted = True

