
infinity = 1e+18

class AlphaBetaGame:
    def __init__(self):
        self.notator = SearchNotator()
        self.seen = {}
        #self.states = dict([(s.name, s) for s in states])
     
    def successors(self, state):
        '''
        state = self.states[state_name]
        for child_state in state.successors:
            yield child_state
        '''
        for child in position_iterator(canonized):
            child_rep = SearchNotator().to_str(child)
            print "Successor pos: %s" % child_rep
            yield child.to_str()


    def utility(self, state, player):
        if self.solved(state):
            return self.saved_value(state)
        if self.terminal_test(state):
            return -infinity
        return 0

    def terminal_test(self, state):
        return len(self.states[state].successors) == 0

    def to_move(self, state):
        return True # TODO?

    #### 

    def solved(self, state):
        return False #TODO
