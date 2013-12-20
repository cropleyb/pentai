from defines import *
from priority_filter import *
from board_strip import *
from length_lookup_table import *

# TODO: move this to test code?
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

            # TODO: move this to test code?
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

    def __repr__(self):
        return "Lines: %s, Takes: %s, Threats: %s, Best: %s" % \
                (self.lines, self.takes, self.threats, self.search_filter)

    def report_length_candidate(self, colour, length, ind_list, inc):
        self.lines[colour][length-1] += inc
        pos_list = []
        for i in ind_list:
            pos = self.ind_to_pos(i)
            pos_list.append(pos)
        if len(pos_list) > 0:
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
    
    def set_or_reset_occs(self, brd, rules, pos, inc):
        # update substrips

        ccp = rules.can_capture_pairs
        for ds in brd.get_direction_strips():
            # Keep track of the lengths of lines that can form 5
            # in a row
            brd_size = brd.get_size()

            bs, s_num = ds.get_strip(pos)
            ind = ds.get_index(pos)

            strip_min, strip_max = ds.get_bounds(s_num, brd_size)

            self.set_ind_to_pos(ds.get_pos, s_num)

            # These are the absolute indices that bound the strip
            # that we want to use to adjust length stats.
            min_ind = max(strip_min, ind-4) # TODO: constants
            max_ind = min(ind+4, strip_max) # inclusive

            # These have different parameter lists because of the different
            # lengths of the matching required.
            # TODO move min_ind into process_substrips
            process_substrips(bs, min_ind, max_ind, self, inc)

            if ccp:
                process_takes(bs, ind, strip_min, strip_max, self, inc)
                process_threats(bs, ind, strip_min, strip_max, self, inc)

