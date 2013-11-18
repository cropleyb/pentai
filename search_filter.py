from search_order import *

class FilterIterator():
    def __init__(self, board_size):
        self.board_size = board_size
        self.left_min = board_size / 2 - 2
        self.lower_min = board_size / 2 - 2
        self.right_max = board_size / 2 + 2
        self.upper_max = board_size / 2 + 2
        self.pos_iter = PosIterator(self.board_size)

    def clone(self):
        newfi = FilterIterator(0) # size is irrelevant
        newfi.left_min = self.left_min
        newfi.lower_min = self.lower_min
        newfi.right_max = self.right_max
        newfi.upper_max = self.upper_max
        newfi.pos_iter = self.pos_iter
        return newfi

    def widen(self, pos):
        new_l_min = pos[0] - 2
        if new_l_min < self.left_min:
            self.left_min = new_l_min
        else:
            new_r_max = pos[0] + 2
            if new_r_max > self.right_max:
                self.right_max = new_r_max
        new_lower_min = pos[1] - 2
        if new_lower_min < self.lower_min:
            self.lower_min = new_lower_min
        else:
            new_upper_max = pos[1] + 2
            if new_upper_max > self.upper_max:
                self.upper_max = new_upper_max

    def get_iter(self):
        pi = self.pos_iter.get_iter()

        for pos in pi:
            if pos[0] >= self.left_min and \
               pos[0] <= self.right_max and \
               pos[1] >= self.lower_min and \
               pos[1] <= self.upper_max:
                yield pos
