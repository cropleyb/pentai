from pentai.base.defines import *

def max_moves_sample_func(depth):
    return 9


class PriorityFilter5(object):
    def __init__(self, orig=None):
        self.reset(orig)

        self.max_moves_func = max_moves_sample_func
        if orig != None:
            self.max_moves_func = orig.max_moves_func
        self.vision = 100

    def set_vision(self, val):
        self.vision = val

    def set_our_colour(self, val):
        pass

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
        return PriorityFilter5(orig=self)

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

    # This isn't being called?!
    def get_captured(self, colour):
        return self.captured[colour]

    def priority_level(self, level, colour):
        return self.candidates_by_priority_and_colour[level][colour]

    '''
Us Them  Our choices
4   4     4X
4   3     4X
4   2     4X
3   4     4O, CX
3   3     3X, 3O, CX, CO, TX
3   2     3X, 2X, 2O, CX, TX
2   3     3O, CX, CO, TX
2   2     2X, 2O, CX, TX
2   1     2X, 1X, CX, TX
1   2     2O, CX, TX
1   1     1X, CX, TX
    '''

    def get_priority_levels(self, our_colour, depth):
        their_colour = opposite_colour(our_colour)

        our_fours = self.priority_level(4, our_colour)
        if len(our_fours) > 0:
            # This will win
            return [our_fours], True

        our_captured = self.get_captured(our_colour)
        our_takes = self.priority_level(5, our_colour)
        our_takes_num = len(our_takes)

        if our_captured >= 8 and our_takes_num > 0:
            # This will win too
            return [our_takes], True

        their_fours = self.priority_level(4, their_colour)
        their_fours_num = len(their_fours)

        if their_fours_num > 0:
            if their_fours_num > 1:
                if our_takes_num > 0:
                    # We will lose unless we capture
                    return [our_takes], False
                else:
                    # Might as well block one of them, can't stop 'em all
                    return [their_fours], True

            # We will lose unless we block or capture 
            return [their_fours, our_takes], False

        their_captured = self.get_captured(their_colour)
        their_takes = self.priority_level(5, their_colour)

        if their_captured >= 8 and len(their_takes) > 0:
            # Block their takes, or capture one of the ends of an
            # attacker, or lose
            return [our_takes, their_takes], False

        ret = []
        if our_takes_num > 0:
            ret = [our_takes]

        attack_levels = 0
        length = 3
        while length > 0:
            ours = self.priority_level(length, our_colour)
            if len(ours) > 0:
                # We have some at this length
                if attack_levels < 2:
                    ret.append(ours)
                    attack_levels += 1

            theirs = self.priority_level(length, their_colour)
            if len(theirs) > 0:
                # They have some at that length:
                ret.append(theirs)
                break

            length -= 1

        if depth < 3:
            if length == 3:
                # We need to cover defending our threatened pairs,
                # but only if we haven't covered them with twos already.
                their_takes_num = len(their_takes)
                if their_takes_num > 0:
                    ret.append(their_takes)

            our_threats = self.priority_level(0, our_colour)
            ret.append(our_threats)

        return ret, False

    def get_iter(self, our_colour, state=None, depth=0, min_priority=0, tried={}): # min_priority is ignored
        their_colour = opposite_colour(our_colour)
        candidate_slots, one_poss = self.get_priority_levels(our_colour, depth)
        
        tried = set()
        for slot in candidate_slots:
            slot_arr = slot.iteritems()
            sorted_slot = [(count, pos) for (pos, count) in slot_arr]
            sorted_slot.sort(reverse=True)
            for count, pos in sorted_slot:
                if count > 0:
                    if not pos in tried:
                        if self.vision < 100:
                            if random.random() * 100 > self.vision:
                                # Can't see that sorry ;)
                                continue
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

    def add_or_remove_candidates(self, colour, length, subtype, pos_list, inc=1):
        if length == 5:
            # won already, ignore
            return
        slot = self.candidates_by_priority_and_colour[length][colour]
        for pos, new_subtype in pos_list:
            assert pos[0] >= 0
            assert pos[1] >= 0
            # Try this for a hack
            if new_subtype == 2 or (length == 2 and new_subtype == 1):
                self.adjust_slot(slot, pos, inc)

    def add_or_remove_take(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        slot = self.candidates_by_priority_and_colour[5][colour]
        self.adjust_slot(slot, pos, inc)

    def add_or_remove_threat(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        slot = self.candidates_by_priority_and_colour[0][colour]
        self.adjust_slot(slot, pos, inc)
