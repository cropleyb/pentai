
class UtilityFilter(object):
    def __init__(self, filt, max_moves):
        self.ab_game = None
        self.filt = filt
        self.max_moves = max_moves

    def set_game(self, ab_game):
        self.ab_game = ab_game

    def copy(self):
        new_filt = self.filt.copy()
        uf = UtilityFilter(new_filt, self.max_moves)
        uf.set_game(self.ab_game)
        return uf

    def __getattr__(self, key):
        return getattr(self.filt, key)

    def utility(self, state, move):
        # Make the state to evaluate it
        child = state.create_state(move)

        # Use ab_game to take advantage of transposition table;
        # only need depth to trigger that.
        return self.ab_game.utility(child, 4)

    def get_iter(self, colour, state, *args, **kwargs):

        l = list(self.filt.get_iter(colour, *args, **kwargs))

        sl = [(self.utility(state, m), m) for m in l]
        our_move = state.is_our_turn()
        sl.sort(reverse=our_move)

        for val, m in sl:
            yield m
