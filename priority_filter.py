from defines import *

class PriorityFilter():
    def __init__(self, orig=None, min_priority=0):
        self.tried = set()

        self.candidates_by_priority_and_colour = []
        cbpc = self.candidates_by_priority_and_colour
        if orig != None:
            ocbpc = orig.candidates_by_priority_and_colour

        for priority in range(6):
            l = []
            cbpc.append(l)
            for colour in range(3):
                if priority < min_priority or orig is None:
                    l.append({})
                else:
                    l.append(ocbpc[priority][colour].copy())


    def copy(self, min_priority=0):
        return PriorityFilter(orig=self, min_priority=min_priority)

    def get_iter(self, our_colour, min_priority=0):
        other_colour = opposite_colour(our_colour)

        cbpc = self.candidates_by_priority_and_colour
        for length in range(1 + 5 - min_priority): # TODO constants
            priority = 5 - length
            cand_for_priority = cbpc[priority]
            for colour in (our_colour, other_colour):
                slot = cand_for_priority[colour]
                slot_arr = slot.iteritems()
                sorted_slot = [(count, pos) for (pos, count) in slot.iteritems()]
                sorted_slot.sort()
                sorted_slot.reverse()
                for count, pos in sorted_slot:
                    if count > 0:
                        if not pos in self.tried:
                            self.tried.add(pos)
                            yield pos
                            # HACK
                            if len(self.tried) > 7:
                                return

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
            slot[pos] = slot.setdefault(pos, 0) + inc
            # Remove - still a value of 0 here, which is ignored in get_iter()

    def add_or_remove_take(self, colour, pos, inc=1):
        # Valuing captures between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc

    def add_or_remove_threat(self, colour, pos, inc=1):
        # Valuing captures between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc
