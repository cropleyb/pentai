from pentai.base.defines import *

def max_moves_sample_func(depth):
    return 9


class PriorityFilter2(object):
    def __init__(self, orig=None):
        self.reset(orig)

        self.max_moves_func = max_moves_sample_func
        if orig != None:
            self.max_moves_func = orig.max_moves_func

    def reset(self, orig=None):
        if orig != None:
            ocbpc = orig.candidates_by_priority_and_colour
        self.captured = [None, 0, 0]
        self.candidates_by_priority_and_colour = []
        cbpc = self.candidates_by_priority_and_colour

        for priority in range(6):
            l = []
            cbpc.append(l)
            for colour in range(3):
                if orig is None:
                    l.append({})
                else:
                    l.append(ocbpc[priority][colour].copy())

    def copy(self):
        return PriorityFilter2(orig=self)

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
        return self.captured[colour]

    def priority_level(self, level, colour):
        return self.candidates_by_priority_and_colour[level][colour]

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

    def get_priority_levels(self, our_colour):
        their_colour = opposite_colour(our_colour)

        our_fours = self.priority_level(5, our_colour)
        if len(our_fours) > 0:
            # This will win
            return [our_fours], True

        our_captures = self.get_captured(our_colour)
        our_takes = self.priority_level(4, our_colour)

        if our_captures >= 8 and len(our_takes) > 0:
            # This will win too
            return [our_takes], True

        their_captures = self.get_captured(their_colour)
        their_takes = self.priority_level(4, their_colour)

        if their_captures >= 8 and len(their_takes) > 0:
            # Block their takes, or capture one of the ends of an
            # attacker, or lose
            return [our_takes, their_takes], False

        their_fours = self.priority_level(5, their_colour)

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

        # if len(their_takes) > 0:
        our_threes = self.priority_level(3, our_colour)
        their_threes = self.priority_level(3, their_colour)
        our_threats = self.priority_level(2, our_colour)
        their_threats = self.priority_level(2, their_colour)

        ret = [our_takes, their_takes, our_threes, their_threes, our_threats, their_threats]

        #if len(their_threes) > 3 or len(their_threats) > 2 or len(our_threes) > 1 or len(our_threats) > 2:
        if len(their_threes) > 3 or len(their_takes) > 1 or len(our_threes) > 2 or len(our_takes) > 1:
            return ret, False

        our_twos = self.priority_level(1, our_colour)
        their_twos = self.priority_level(1, their_colour)

        ret.extend([our_twos, their_twos])

        if len(their_twos) > 3 or len(their_threats) > 1 or len(our_twos) > 2 or len(our_threats) > 1:
            return ret, False

        ret = []
        for level in range(4, -1, -1):
            for colour in [our_colour, their_colour]:
                ret.append(self.priority_level(level, colour))
        return ret, False

    def get_iter(self, our_colour, depth=0, min_priority=0, tried={}): # min_priority is ignored
        their_colour = opposite_colour(our_colour)
        candidate_slots, one_poss = self.get_priority_levels(our_colour)
        
        tried = set()
        for slot in candidate_slots:
            slot_arr = slot.iteritems()
            sorted_slot = [(count, pos) for (pos, count) in slot_arr]
            sorted_slot.sort(reverse=True)
            for count, pos in sorted_slot:
                if count > 0:
                    if not pos in tried:
                        tried.add(pos)
                        yield pos
                        if one_poss:
                            return
                        if len(tried) >= self.max_moves_func(depth):
                            return

    def __repr__(self):
        return "%s" % self.candidates_by_priority_and_colour[5]

    def adjust_slot(self, slot, pos, inc):
        slot[pos] = slot.setdefault(pos, 0) + inc
        if slot[pos] == 0:
            del slot[pos]

    def add_or_remove_candidates(self, colour, length, pos_list, inc=1):
        if length == 5:
            # won already, ignore
            return
        if length == 4: # allow space for take priority
            length = 5
        if length < 3:  # allow space for threat priority
            length -= 1
        slot = self.candidates_by_priority_and_colour[length][colour]
        for pos in pos_list:
            assert pos[0] >= 0
            assert pos[1] >= 0
            self.adjust_slot(slot, pos, inc)

    def add_or_remove_take(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing takes between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        self.adjust_slot(slot, pos, inc)

    def add_or_remove_threat(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing threats between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        self.adjust_slot(slot, pos, inc)
