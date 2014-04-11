from pentai.base.pente_exceptions import *
from pentai.base.defines import *
import pentai.ai.ab_game as abg_m
import pentai.ai.alpha_beta as ab_m
import pentai.ai.openings_mover as om_m
import pentai.base.player as p_m
import pentai.ai.utility_calculator as uc_m

import random
import threading

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
        return self.genome == other.genome

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
        guess = max(self.max_depth-3, 1)
        guess *= self.genome.vision / 100.0
        guess *= self.genome.judgement / 100.0
        return guess

    def attach_to_game(self, base_game):
        # Super requires inheriting from object, which clashes with pickle?!
        #super(AIPlayer, self).attach_to_game(base_game)
        p_m.Player.attach_to_game(self, base_game)
        self.ab_game = abg_m.ABGame(self, base_game)
        self.openings_mover = None

    def prompt_for_action(self, base_game, gui, test=False):
        if test:
            return self.do_the_search()
        else:
            # TODO: platform dependent choice?
            try:
                self.do_search_process(gui)
            except:
                t = threading.Thread(target=self.search_thread, args=(gui,))
                
                # Allow the program to be exited quickly
                t.daemon = True
                
                t.start()

        return "%s is thinking" % self.get_name()

    def get_type(self):
        return "Computer"

    def do_search_process(self, gui):
        from search_process import SearchProcess
        game = self.ab_game.base_game
        self.search_process = SearchProcess()
        self.search_process.create_process(game, gui)

    def search_thread(self, gui):
        action = self.do_the_search()
        gui.enqueue_action(action)

    def get_openings_mover(self):
        if self.openings_mover is None:
            # ie first run through
            self.openings_mover = om_m.OpeningsMover(
                    self.openings_book, self.ab_game.base_game)
        return self.openings_mover

    def make_opening_move(self, seen):
        if self.use_openings_book():
            base_game = self.ab_game.base_game

            om = self.get_openings_mover()
            move = om.get_a_good_move(self, seen)
            if move:
                return move

    def do_the_search(self):
        try:
            return self.do_the_search_inner()
        except NoMovesException:
            self.ab_game.base_game.set_won_by(BLACK+WHITE)

    def do_the_search_inner(self):
        ab_game = self.ab_game

        seen = set()
        move = self.make_opening_move(seen)
        rules = ab_game.get_rules()
        turn = ab_game.get_move_number()
        while move or (turn == 3):
            if move:
                if ab_game.base_game.get_board().get_occ(move) != EMPTY:
                    print "Corrupt opening %s suggestion ignored" % (move,)
                else:
                    if turn != 3 or not rules.move_is_too_close(move):
                        return move
            x = random.randrange(-4, 5) + rules.size / 2
            y = random.randrange(-4, 5) + rules.size / 2
            move = (x, y)

        ab_ss = ab_game.current_state
        if len(seen) < 2:
            ab_ss.set_seen(seen)
        thinking_in_opponents_move = (ab_ss.get_state().to_move_player() != self)

        if thinking_in_opponents_move:
            st()
            last_move_state = ab_game.current_state.clone()
            last_move_state.go_backwards_one()
            ab_ss = ABState(last_move_state)
            #current_tt = {}
            #old_tt = current_tt # FIXME
            ab_game.transposition_table = {}
            prev_tt = {}
            # TODO: depth + 1
        # else don't adjust tt
        i = 0
        while i < 2:
            #move, value = ab_m.alphabeta_search(ab_game.current_state, ab_game)
            move, value = ab_m.alphabeta_search(ab_ss, ab_game)
            if self.ab_game.interrupted:
                if thinking_in_opponents_move:
                    # Fill it out as well as we can.
                    ab_game.transposition_table = \
                            old_tt.update(ab_game.transposition_table)
                return
            if not thinking_in_opponents_move:
                # Just one iteration
                break
            # Merge in the latesttable
            prev_tt = prev_tt.update(ab_game.transposition_table)
            # Next time, start from scratch
            ab_game.transposition_table = {}
            # TODO: Increase the depth level by 2

            i += 1

        action = move[0]

        '''
        print "size of transposition table: %s" % len(ab_game.transposition_table)
        '''
        if not thinking_in_opponents_move:
            # Don't reset if we have "thinking in opponents time" turned on
            ab_game.reset_transposition_table()

        # TODO: if we were thinking in the opponent's time, return nothing

        #print " => %s" % (action,)
        return action

    def set_interrupted(self):
        self.ab_game.interrupted = True
        if self.search_process != None:
            self.search_process.kill()
