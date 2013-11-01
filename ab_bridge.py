#!/usr/bin/python

import board
import state

'''
class Move():
    def __init__(self, pos):
        self.pos = pos
    def position(self):
        return self.pos

class Pos():
    def __init__(self, x, y):
        self.tup = (x,y)
    def __getitem__(self, dim):
        return self.tup[dim]
    def shift(self, direction, steps):
        new_pos = (self.tup[0] + (direction[0] * steps), \
                   self.tup[1] + (direction[1] * steps)) 
        return Pos(new_pos)
'''

class ABState():
    """ Bridge for state, for use by alpha_beta code """
    def __init__(self, parent=None, move=None):
        s = None
        if parent:
            s = parent.state
        self.state = state.State(s, move)

    def to_move(self):
        return self.state.to_move()

    def __repr__(self):
        return self.state.__repr__()

    def utility(self, player):
        return self.state.utility(player)

    def score(self):
        return self.utility(None)


class ABGame():
    """ This class acts as a bridge between the AlphaBeta code and my code """
    def __init__(self, size):
        self.board = board.Board(size)
        # TEMP HACK
        #global BOARD_SIZE
        #BOARD_SIZE = size
        self.current_state = ABState()

    def to_move(self, state=None):
        if state is None:
            state = self.current_state
        return state.to_move()

    def make_move(self, x, y):
        self.current_state.set_colour(Pos(x,y), 1)

    def utility(self, state, player):
        return state.utility(player)

    def successors(self, state):
        for succ in state.state.successors():
            yield ABState(succ) # TODO: move
        '''
        succ = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                pos = (x, y)
                action = Move(pos)
                try:
                    succ.append((action, state.State(state, action)))
                except IllegalMoveException:
                    pass
        return succ
        '''

    def terminal_test(self, state):
        return False
        # return len(self.successors(state)) == 0 THIS causes mass delay

if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    g = ABGame(7)

    #pdb.set_trace()
    alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
