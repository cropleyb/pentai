from pentai.base.defines import *
from pentai.ai.search_order_table import *

import copy

def max_moves_sample_func(depth):
    return 9


class PriorityFilter4(object):
    def __init__(self, orig=None):
        self.reset(orig)

        self.max_moves_func = max_moves_sample_func
        if orig != None:
            self.max_moves_func = orig.max_moves_func
        self.vision = 100

    def set_vision(self, val):
        self.vision = val

    def set_our_colour(self, colour):
        self.colour = colour

        psi = get_priority_slot_index(True, 4, 0, 0)
        self.our_fours  = self.priority_level(psi)
        psi = get_priority_slot_index(False, 4, 0, 0)
        self.their_fours = self.priority_level(psi)

        #st()
        self.our_takes = self.priority_level(take_psi[True]) # True -> us
        self.their_takes = self.priority_level(take_psi[False])

    def reset(self, orig=None):
        if orig != None:
            ocbpc = orig.candidates_by_priority

            self.candidates_by_priority = copy.deepcopy(ocbpc)
            self.captured = copy.deepcopy(orig.captured)
            self.set_our_colour(orig.colour)
        else:
            # TODO: Test this in interpreter
            self.candidates_by_priority = [{} for i in range(len(psi_table))]
            self.set_our_colour(P1) # TODO!
            self.captured = [0, 0] # Is this ever set???


        '''
        cbpc = self.candidates_by_priority
        # TODO: Time these
        for priority in range(6):
            l = []
            cbpc.append(l)
            for colour in range(3):
                if orig is None:
                    l.append({})
                else:
                    l.append(ocbpc[priority][colour].copy())
        '''

    def copy(self):
        return PriorityFilter4(orig=self)

    def set_vision(self, val):
        self.vision = val

    def set_max_moves_func(self, mmf):
        self.max_moves_func = mmf

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

    def get_captured(self, colour):
        is_us = (colour == self.colour)
        return self.captured[is_us]

    def priority_level(self, order_index):
        return self.candidates_by_priority[order_index]

    '''
    # TODO?
    Opponent Min response
    biggest  length
    threat
    ------------------------
    2+x 4    win or take
    1 x 4    win, block or take
    take     create 3 type 1 or 2 (3), block 3?
    3+ x 3   block or threaten (adjust 3+ threshold?)
    1|2 x 3  block or threaten, or attack with 2->3
    threat   defend
    2        
    1
    n        n-1? for opponent?
    '''

    def get_priority_levels(self, is_us):
        our_fours = self.our_fours
        if len(our_fours) > 0:
            # This will win
            return [our_fours], True

        our_captured = self.captured[is_us]
        our_takes = self.our_takes

        if our_captured >= 8 and len(our_takes) > 0:
            # This will win too
            return [our_takes], True

        their_captured = self.captured[not is_us]
        their_takes = self.their_takes

        if their_captured >= 8 and len(their_takes) > 0:
            # Block their takes, or capture one of the ends of an
            # attacker, or lose
            return [our_takes, their_takes], False

        their_fours = self.their_fours

        if len(their_fours) > 0:
            if len(their_fours) > 1:
                if len(our_takes) > 0:
                    # We will lose unless we capture
                    return [our_takes], False
                else:
                    # Might as well block one of them, can't stop 'em all
                    return [their_fours], True

            # We will lose unless we block or capture 
            return [their_fours, our_takes], False

        search_order = search_order_us
        if not is_us:
            search_order = search_order_them

        ret = []
        for psi in search_order[2:]:
            ret.append(self.candidates_by_priority[psi])

        return ret, False

    def get_iter(self, our_colour, state=None, depth=0, min_priority=0, tried={}): # min_priority is ignored
        their_colour = opposite_colour(our_colour)
        is_us = (our_colour==self.colour)
        candidate_slots, one_poss = self.get_priority_levels(is_us)
        
        tried = set()
        for slot in candidate_slots:
            slot_arr = slot.iteritems()
            sorted_slot = [(count, pos) for (pos, count) in slot_arr]
            sorted_slot.sort(reverse=True)
            for count, pos in sorted_slot:
                if count > 0:
                    if not pos in tried:
                        if self.vision < 100:
							# TODO: make sure set_vision is called for PF2
                            if random.random() * 100 > self.vision:
                                # Can't see that sorry ;)
                                continue
                        tried.add(pos)
                        yield pos
                        if one_poss:
                            return
                        if len(tried) >= self.max_moves_func(depth):
                            return

    '''
    def __repr__(self):
        return "%s" % self.candidates_by_priority
    '''

    def adjust_slot(self, slot, pos, inc):
        slot[pos] = slot.setdefault(pos, 0) + inc
        if slot[pos] == 0:
            del slot[pos]

    def add_or_remove_candidates(self, colour, length, sub_type, pos_list, inc=1):
        # TODO: pass in is_us?
        is_us = (colour == self.colour)
        #print "Subtype is %s" % sub_type

        for pos, ns in pos_list:
            assert pos[0] >= 0
            assert pos[1] >= 0
            psi = get_priority_slot_index(is_us, length, sub_type, ns)
            slot = self.candidates_by_priority[psi]
            self.adjust_slot(slot, pos, inc)

    def add_or_remove_take(self, colour, pos, inc=1):
        # TODO: pass in is_us?
        is_us = (colour == self.colour)

        assert pos[0] >= 0
        assert pos[1] >= 0
        # Searching takes between 3s and 4s
        psi = take_psi[is_us]
        slot = self.candidates_by_priority[psi]
        self.adjust_slot(slot, pos, inc)

    def add_or_remove_threat(self, colour, pos, inc=1):
        # TODO: pass in is_us?
        is_us = (colour == self.colour)

        assert pos[0] >= 0
        assert pos[1] >= 0
        # Searching threats between 2s and 3s
        psi = threat_psi[is_us]
        slot = self.candidates_by_priority[psi]
        self.adjust_slot(slot, pos, inc)
