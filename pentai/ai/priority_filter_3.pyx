from pentai.base.defines import *

import random

def max_moves_sample_func(depth):
    return 9

class PriorityFilter3(object):
    def __init__(self, orig=None, min_priority=0):

        self.max_moves_func = max_moves_sample_func
        if orig != None:
            self.max_moves_func = orig.max_moves_func
        self.vision = 100

        self.reset(orig, min_priority)

    def set_vision(self, val):
        self.vision = val

    def set_max_moves_per_depth_level(self, mmpdl, narrowing, chokes=[]):
        if narrowing != 0:
            def mmpdl_func(depth):
                # This is really hacky, but it seemed to work
                for d, w in chokes:
                    if depth >= d:
                        return w
                return mmpdl - round(narrowing * depth)
        else:
            def mmpdl_func(depth):
                # This is really hacky, but it seemed to work
                for d, w in chokes:
                    if depth >= d:
                        return w
                return mmpdl

        self.set_max_moves_func(mmpdl_func)

    def reset(self, orig=None, min_priority=0):
        if orig != None:
            ocbpc = orig.candidates_by_priority_and_colour
        self.candidates_by_priority_and_colour = []
        cbpc = self.candidates_by_priority_and_colour

        for priority in range(6):
            l = []
            cbpc.append(l)
            for colour in range(3):
                if priority < min_priority or orig is None:
                    l.append({})
                else:
                    l.append(ocbpc[priority][colour].copy())

        if orig:
            self.move_counts = orig.move_counts.copy()
        else:
            self.move_counts = {}

    def set_max_moves_func(self, mmf):
        self.max_moves_func = mmf

    def copy(self, min_priority=0):
        return PriorityFilter3(orig=self, min_priority=min_priority)

    def get_iter(self, our_colour, depth=0, min_priority=0, tried=None):
        if tried is None:
            tried = set()
        other_colour = opposite_colour(our_colour)

        cbpc = self.candidates_by_priority_and_colour
        for length in range(1 + 5 - min_priority): # TODO constants
            priority = 5 - length
            cand_for_priority = cbpc[priority]
            for colour in (our_colour, other_colour):
                slot = cand_for_priority[colour]
                slot_arr = slot.iteritems()
                sorted_slot = [ \
                            (list(self.get_all_priorities(pos, \
                            our_colour)), pos) \
                            for pos, count in slot_arr \
                            if count and (not pos in tried)]
                sorted_slot.sort(reverse=True)
                for counts, pos in sorted_slot:
                    if counts:
                        if not pos in tried:
                            if self.vision < 100:
                                if random.random() * 100 > self.vision:
                                    # Can't see that sorry ;)
                                    continue
                            tried.add(pos)
                            yield pos
                            if len(tried) >= self.max_moves_func(depth):
                                return

    def __repr__(self):
        return "%s" % self.candidates_by_priority_and_colour[5]

    def get_all_priorities(self, pos, our_colour):
        move_slot = self.move_counts[pos]

        for i in range(6):
            # We're black: 0
            # We're white: 1
            ind = 2 * i + (our_colour - 1)
            yield move_slot[ind]

            # We're black: 1
            # We're white: 0
            ind = 2 * i + (2 - our_colour)
            yield move_slot[ind]


    def add_move_count(self, colour, length, pos, inc):
        try:
            move_slot = self.move_counts[pos]
        except KeyError:
            l = [0] * 12
            move_slot = self.move_counts[pos] = l

        ind = 9 + colour - (length * 2)
        move_slot[ind] += inc

    def add_or_remove_candidates(self, colour, length, pos_list, inc=1):
        if length == 5:
            # won already, ignore
            return
        if length == 4: # allow space for capture priority
            length = 5
        if length < 3:  # allow space for threat priority
            length -= 1
        slot = self.candidates_by_priority_and_colour[length][colour]
        for pos in pos_list:
            assert pos[0] >= 0
            assert pos[1] >= 0
            slot[pos] = slot.setdefault(pos, 0) + inc
            # Remove - still a value of 0 here, which is ignored in get_iter()
            
            self.add_move_count(colour, length, pos, inc)

    def add_or_remove_take(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing captures between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc
        self.add_move_count(colour, 4, pos, inc)

    def add_or_remove_threat(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing captures between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc
        self.add_move_count(colour, 2, pos, inc)
