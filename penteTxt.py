#!/usr/bin/python

import alpha_beta
import ab_bridge

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

if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print "(without psyco)"

    g = Game(7)

    #pdb.set_trace()
    alpha_beta.alphabeta_search(g.current_state, g, max_depth=1)
    
