from defines import *

class UtilityStats():

    def __init__(self, parent=None):
        if parent == None:
            self.lines = [None, [0] * 5, [0] * 5]
            self.takes = [0, 0, 0]
            self.threats = [0, 0, 0]
            self.search_filter = None # TODO: use
        else:
            pl = parent.lines
            # Manual deep copy
            self.lines = [None, pl[BLACK][:], pl[WHITE][:]]
            self.takes = parent.takes[:]
            self.threats = parent.threats[:]
            #self.search_filter = parent.search_filter.copy() TODO

    def report_length_candidate(self, colour, length, ind_list, inc):
        self.lines[colour][length-1] += inc

    def report_take(self, colour, ind, inc):
        self.takes[colour] += inc
        
    def report_threat(self, colour, ind, inc):
        self.threats[colour] += inc
        
    def set_ind_to_pos(self, func):
        self.ind_to_pos = func

