from defines import *
from priority_filter import *

def pass_through_func(a, ignored):
    """ This is just a stub, shouldn't be called in production code. """
    return (a, 0)

class UtilityStats():

    def __init__(self, parent=None):
        if parent == None:
            self.lines = [None, [0] * 5, [0] * 5]
            self.takes = [0, 0, 0]
            self.threats = [0, 0, 0]
            self.search_filter = PriorityFilter()
            self.i_to_p = pass_through_func
            self.s_num = 0 # irrel, just needs a value
        else:
            pl = parent.lines
            # Manual deep copy
            self.lines = [None, pl[BLACK][:], pl[WHITE][:]]
            self.takes = parent.takes[:]
            self.threats = parent.threats[:]
            # TODO: Use depth and/or min priority when copying the search filter
            self.search_filter = parent.search_filter.copy()
            self.s_num = 0 # irrel, just needs a value

    def report_length_candidate(self, colour, length, ind_list, inc):
        self.lines[colour][length-1] += inc
        pos_list = []
        for i in ind_list:
            pos = self.ind_to_pos(i)
            pos_list.append(pos)
        self.search_filter.add_or_remove_candidates(
                colour, length, pos_list, inc)

    def report_take(self, colour, ind, inc):
        self.takes[colour] += inc
        pos = self.ind_to_pos(ind)
        self.search_filter.add_or_remove_take(colour, pos, inc)
        
    def report_threat(self, colour, ind, inc):
        self.threats[colour] += inc
        pos = self.ind_to_pos(ind)
        self.search_filter.add_or_remove_threat(colour, pos, inc)

    def ind_to_pos(self, ind):
        return self.i_to_p(ind, self.s_num)
     
    def set_ind_to_pos(self, func, s_num):
        # These two should always be set together
        self.i_to_p = func
        self.s_num = s_num

