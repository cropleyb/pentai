from pentai.base.defines import INFINITY
from pentai.base.pente_exceptions import *

INF = INFINITY, 0
NEGINF = -INFINITY, 0

debug=False

def argmax(aspi, fn):
    """ aspl: action state pair list
    """
    best = -INFINITY, None
    try:
        curr_state = aspi.next()
    except StopIteration:
        raise NoMovesException()

    try:
        next_state = aspi.next()
    except StopIteration:
        # Don't bother searching, there is only one move
        # TODO: This is assuming that there is only one move because
        # they have been correctly prioritised, and that the value
        # returned by the search is irrelevant.
        return curr_state, 0

    val = fn(curr_state)
    best = val, curr_state

    curr_state = next_state
    val = fn(curr_state)
    if val > best[0]:
        best = val, curr_state

    for curr_state in aspi:
        val = fn(curr_state)
        if val > best[0]:
            best = val, curr_state

    return best[1], best[0]

def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return game.utility(state, depth)
        v = NEGINF
        for (a, s) in game.successors(state, depth):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                game.report_short_circuit(a, depth)
                break
            if v > (INFINITY/100.0, 0):
                # Game won, can't get better
                game.report_short_circuit(a, depth)
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
                game.report_short_circuit(a, depth)
                break
            if v < (-INFINITY/100.0, 0):
                # Game lost, can't get worse
                game.report_short_circuit(a, depth)
                break
            beta = min(beta, v)
        game.save_utility(state, depth, v)
        return v

    def cutoff_test(state, depth):
        # The default test cuts off at depth d or at a terminal state
        return game.terminal_test(state, depth)

    def top_min_func(pair):
        a, s = pair
        return min_value(s, NEGINF, INF, 1)

    # Body of alphabeta_search starts here:
    action, value = argmax(game.successors(state, 1), top_min_func)
    return action, value

