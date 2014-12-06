from pentai.base.pente_exceptions import *
from pentai.base.defines import *
import pentai.base.logger as log
import pentai.ai.ab_game as abg_m
import pentai.ai.alpha_beta as ab_m
import pentai.ai.openings_mover as om_m
import pentai.base.player as p_m
import pentai.ai.utility_calculator as uc_m

import threading

from kivy import platform

skip_openings_book = False
def set_skip_openings_book(val):
    skip_openings_book = val

class AIPlayer(p_m.Player):
    """ Yes there is a circular dependancy between AIPlayer and Game """

    def __init__(self, search_filter, *args, **vargs):

        self.max_depth = 1
        self.search_filter = search_filter
        self.genome = None # temp hack
        self.openings_book = None
        self.openings_mover = None

        self.utility_calculator = uc_m.UtilityCalculator()

        self.search_process = None
        # Super requires inheriting from object, which clashes with pickle?!
        #return super(AIPlayer, self).__init__(*args, **vargs)
        return p_m.Player.__init__(self, *args, **vargs)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.genome == other.genome

    def use_openings_book(self):
        return not (self.openings_book is None) and not skip_openings_book

    def set_use_openings_book(self, openings_book):
        self.openings_book = openings_book

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth
    
    def get_utility_calculator(self):
        return self.utility_calculator

    def get_priority_filter(self):
        return self.search_filter

    def get_rating(self):
        # Min: 100 for "max_depth": 1, "judgement": 10, "vision": 10,
        # Max: 1900 for "max_depth": 10, "judgement": 100, "vision": 100,
        mult = self.genome.vision * self.genome.judgement * self.max_depth
        guess = mult / 52.6
        return guess

    def attach_to_game(self, base_game):
        # Super requires inheriting from object, which clashes with pickle?!
        #super(AIPlayer, self).attach_to_game(base_game)
        p_m.Player.attach_to_game(self, base_game)
        self.ab_game = abg_m.ABGame(self, base_game)
        if self.genome.utility_filter:
            self.search_filter.set_game(self.ab_game)

        self.openings_mover = None
        our_colour = base_game.get_colour_of_player(self)
        self.search_filter.set_our_colour(our_colour)

    def prompt_for_action(self, base_game, gui, test=False):
        if test:
            return self.do_the_search()
        else:
            if platform == "osx":
                # TODO: Linux is probably OK (#16)
                # TODO: Windows should be fixable (#1)
                try:
                    self.do_search_process(gui)
                    return
                except ImportError:
                    pass
            t = threading.Thread(target=self.search_thread, args=(gui,))
            
            # Allow the program to be exited quickly
            t.daemon = True
            
            t.start()

        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "AI"

    def do_search_process(self, gui): # TODO: We shouldn't know about the gui
        from search_process import SearchProcess
        game = self.ab_game.base_game
        self.search_process = SearchProcess(gui)
        self.search_process.create_process(game)

    def search_thread(self, gui):
        action = self.do_the_search()
        gui.enqueue_action(action)

    def get_openings_mover(self):
        if self.openings_mover is None:
            # ie first run through
            self.openings_mover = om_m.OpeningsMover(
                    self.openings_book, self.ab_game)
        return self.openings_mover

    def make_opening_move(self, turn, seen):
        if turn > 8: # TODO: Use OPENINGS_DEPTH constant - but where should it live???
            return
        if self.use_openings_book():
            log.info("Looking for an opening book move")
            base_game = self.ab_game.base_game

            om = self.get_openings_mover()
            move = om.get_a_good_move(self, seen)
            if move:
                log.info("Used an opening book move")
                return move
            else:
                log.info("Didn't find an opening book move")

    def do_the_search(self):
        try:
            return self.do_the_search_inner()
        except NoMovesException:
            self.ab_game.base_game.set_won_by(P1+P2)

    def do_the_search_inner(self):
        ab_game = self.ab_game

        seen = set()
        turn = ab_game.get_move_number()
        prev_move = ab_game.get_last_move()
        move = self.make_opening_move(turn, seen)
        rules = ab_game.get_rules()

        if move:
            if ab_game.base_game.get_board().get_occ(move) != EMPTY:
                log.info("Corrupt opening %s suggestion ignored" % (move,))
            else:
                assert(turn != 3 or not rules.move_is_too_close(move))
                print "chose opening move"
                return turn, prev_move, move

        ab_ss = ab_game.current_state

        # What is this for? No tests break without it?
        if len(seen) < 2:
            ab_ss.set_seen(seen)

        move, value = ab_m.alphabeta_search(ab_ss, ab_game)
        if self.ab_game.was_interrupted():
            log.info("Game was interrupted")
            return None

        action = move[0]

        '''
        log.info("size of transposition table: %s" % len(ab_game.transposition_table))
        '''
        ab_game.reset_transposition_table()

        #log.info(" => %s" % (action,))
        return turn, prev_move, action

    def stop(self):
        if self.search_process != None:
            # TODO: Reset the queue, as it could be corrupted by this
            self.search_process.terminate()
            self.search_process = None
