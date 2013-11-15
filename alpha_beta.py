import pdb

infinity = 1e+31

def argmax(aspl, fn):
    """ aspl: action state pair list
    """
    #print "***** In argmax"

    vals = [(fn(item), item) for item in aspl]
    vals.sort()
    # print vals
    best = max(vals)
    return best[1], best[0]

def alphabeta_search(state, game, max_depth=4):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return game.utility(state, player)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return game.utility(state, player)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def cutoff_test(state, depth):
        # The default test cuts off at depth d or at a terminal state
        return depth>max_depth or game.terminal_test(state)

    # print "***** Defining top_min_func"
    def top_min_func((a,s)):
        return min_value(s, -infinity, infinity, 0)

    # Body of alphabeta_search starts here:
    action, value = argmax(game.successors(state), top_min_func)
    return action, value

