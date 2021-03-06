from pentai.base.defines import *
from pentai.base.pente_exceptions import *

cimport cython

def max_moves_sample_func(depth):
    return 9


class PriorityFilter2(object):
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

    # This isn't being called?!
    def get_captured(self, colour):
        return self.captured[colour]

    def priority_level(self, level, colour):
        return self.candidates_by_priority_and_colour[level][colour]

    def always_return_something(self, sugg):
        total_moves = 0
        for r in sugg:
            total_moves += len(r)

        if total_moves > 0:
            return sugg, False
        else:
            # Current player is going to lose. Play a "good" move anyway
            cbpc = self.candidates_by_priority_and_colour
            #[level][colour]
            # HERE
            ret = []
            for level in range(4, -1, -1):
                for colour in [P1, P2]: # Doesn't matter, we're gonna lose anyway
                    ret.append(self.priority_level(level, colour))
            return ret, True

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


        '''
        # This isn't working, yet?

        # a single instance of a double 3 attack must be blocked,
        # captured, or threatened, or we must extend a 3 of our own

        our_threes = self.priority_level(3, our_colour)
        all_their_threes = self.priority_level(3, their_colour)

        their_multi_threes = {}
        for p,count in all_their_threes.iteritems():
            if count > 1:
                their_multi_threes[p] = count

        our_threats = self.priority_level(2, our_colour)
        their_threats = self.priority_level(2, their_colour)

        tmtc = len(their_multi_threes)
        if tmtc > 0:
            # They have at least one place that they can get 2 or more
            # simultaneous 4 attacks.

            # We must capture, threaten it, block
            # there, or extend a 3
            if tmtc < 3:
                # We must capture, threaten it, block
                # there, or extend a 3
                ret = [their_multi_threes]
            else:
                # Can't block all that
                ret = []

            """
            all_their_ones = self.priority_level(1, their_colour)

            for to_pos in all_their_ones:
                for mt_pos in their_multi_threes:
                    # if the pos is near their multi-three, it might be able
                    # to take into two or more 4 lines. Hmmm.
                    if mt_pos
            """

            ret.extend([our_takes, our_threes, our_threats, their_threats, all_their_ones])

            return self.always_return_something(ret)
        '''

        '''
        our_twos = self.priority_level(1, our_colour)

        if len(their_threes) > 2 and len(our_threes) == 0:
            return [their_threes, our_takes, our_threats, their_takes, our_twos], False

        their_twos = self.priority_level(1, their_colour)
        # if len(their_takes) > 0:

        ret = [our_takes, their_takes, our_threes, their_threes, our_threats, their_threats]

        #if len(their_threes) > 3 or len(their_threats) > 2 or len(our_threes) > 1 or len(our_threats) > 2:
        if len(their_threes) > 3 or len(their_takes) > 1 or len(our_threes) > 2 or len(our_takes) > 1:
            return ret, False

        our_twos = self.priority_level(1, our_colour)
        their_twos = self.priority_level(1, their_colour)

        ret.extend([our_twos, their_twos])

        if len(their_threes) > 0 or len(their_takes) > 0 or len(our_threes) > 0 or len(our_takes) > 0:
            return ret, False

        if len(their_twos) > 3 or len(their_threats) > 1 or len(our_twos) > 2 or len(our_threats) > 1:
            return ret, False
        '''

        ret = []
        #print "defaulting to many levels"
        for level in range(4, -1, -1):
            for colour in [our_colour, their_colour]:
                ret.append(self.priority_level(level, colour))
        return ret, False

    def get_iter(self, our_colour, state=None, depth=0, min_priority=0, tried={}): # min_priority is ignored
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
                        if self.vision < 100:
                            if random.random() * 100 > self.vision:
                                # Can't see that sorry ;)
                                print "Blind to that"
                                continue
                        # Check for 2nd P1 move
                        try:
                            if state:
                                # TODO: Rename to check_legality
                                state.is_illegal(pos)
                        except IllegalMoveException:
                            print "Skipping illegal suggestion - probably tournament move restriction"
                            continue

                        tried.add(pos)
                        yield pos
                        if one_poss:
                            #print "one_poss"
                            return
                        if len(tried) >= self.max_moves_func(depth):
                            return

        #if len(tried) == 0:
            #print "No candidates: %s " % candidate_slots
            #raise NoMovesException("In PF2!")

    def __repr__(self):
        return "%s" % self.candidates_by_priority_and_colour[5]

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
            adjust_slot(self, slot, pos, inc)

    def add_or_remove_take(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing takes between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        adjust_slot(self, slot, pos, inc)

    def add_or_remove_threat(self, colour, pos, inc=1):
        assert pos[0] >= 0
        assert pos[1] >= 0
        # Valuing threats between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        adjust_slot(self, slot, pos, inc)

@cython.profile(False)
cdef inline adjust_slot(self, slot, pos, inc):
    slot[pos] = slot.setdefault(pos, 0) + inc
    if slot[pos] == 0:
        del slot[pos]

