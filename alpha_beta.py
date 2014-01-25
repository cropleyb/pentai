from defines import INFINITY
from pente_exceptions import *

INF = INFINITY, 0
NEGINF = -INFINITY, 0

def argmax(aspi, fn):
    """ aspl: action state pair list
    """
    # The original list interpretation was faster but didn't short cut wins
    asp_l = list(aspi)
    if len(asp_l) == 0:
        raise NoMovesException()
    only_one = (len(asp_l) == 1)

    vals = []
    for item in asp_l:
        if only_one:
            # Don't bother searching, there is only one move
            # TODO: This is assuming that there is only one move because
            # they have been correctly prioritised, and that the value
            # returned by the search is irrelevant.
            val = 0
        else:
            val = fn(item)
        vals.append((val, item))
    # sort is for debug presentation only. Since this function is only called
    # once per search, it should not be a problem.
    #print "Deep util"
    #vals.sort()
    #for v in vals:
        #print v
    best = max(vals)
    return best[1], best[0]

def alphabeta_search(state, game, max_depth=4):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return game.utility(state, depth)
        v = NEGINF
        for (a, s) in game.successors(state, depth):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                break
            alpha = max(alpha, v)
        game.save_utility(state, depth, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return game.utility(state, depth)
        v = INF
        for (a, s) in game.successors(state, depth):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                break
            beta = min(beta, v)
        game.save_utility(state, depth, v)
        return v

    def cutoff_test(state, depth):
        # The default test cuts off at depth d or at a terminal state
        return depth>=max_depth or game.terminal_test(state)

    def top_min_func(pair):
        a, s = pair
        return min_value(s, NEGINF, INF, 1)

    # Body of alphabeta_search starts here:
    action, value = argmax(game.successors(state, 1), top_min_func)
    return action, value

