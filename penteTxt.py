#!/usr/bin/python

# TODO
import board
import state


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


class Game():
    def __init__(self, size):
        self.board = Board(size)
        # TEMP HACK
        global BOARD_SIZE
        BOARD_SIZE = size
        self.current_state = state.State()
        #pdb.set_trace()

    def to_move(self, state):
        return state.to_move()

    def make_move(self, x, y):
        self.current_state.set_colour(Pos(x,y), 1)

    def utility(self, state, player):
        return state.utility(player)


    def successors(self, state):
        succ = []
        #pdb.set_trace()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                pos = (x, y)
                action = Move(pos)
                try:
                    succ.append((action, state.State(state, action)))
                except IllegalMoveException:
                    pass
        return succ

    def terminal_test(self, state):
        return False
        # return len(self.successors(state)) == 0 THIS causes mass delay

if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    g = Game(7)

    #pdb.set_trace()
    alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
