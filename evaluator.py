from utility_stats import *
from null_filter import *

class Evaluator():
    """
    This is to help with debugging bad moves.
    """
    def __init__(self, calculator, state):
        self.state = state
        self.calculator = calculator
        calculator.set_rules(self.get_rules())
        self.utility_stats = UtilityStats(parent=None, search_filter=NullFilter())
        state.add_observer(self)
        #self.rules = self.get_rules() # TODO

    def board(self):
        return self.state.board

    def game(self):
        return self.state.game
    
    def get_rules(self):
        return self.game().rules

    def reset_state(self):
        self.utility_stats.reset()

    def before_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs( \
                self.board(), self.get_rules(), pos, -1)

    def after_set_occ(self, pos, colour):
        self.utility_stats.set_or_reset_occs( \
                self.board(), self.get_rules(), pos, 1)

    def search_player_colour(self):
        """ The AI player who is performing the search.
            For the evaluator, we will always show it from one
            player's perspective
        """
        return BLACK
        '''
        game = self.game()
        return game.to_move_colour()
        '''

    def to_move_colour(self):
        return self.state.to_move_colour()

    def get_captured(self, colour):
        return self.state.get_captured(colour)

    def get_move_number(self):
        return self.state.get_move_number()

    def get_takes(self):
        return self.utility_stats.takes

    def set_won_by(self, colour):
        pass

    def utility(self):
        # TODO: self.state is not an ABState instance
        return "Utility for %s: %s (%s)" % ( self.get_move_number(),
                self.calculator.utility(self, self.utility_stats),
                self.utility_stats)
