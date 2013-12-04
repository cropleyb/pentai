from defines import *

class PriorityFilter():
    def __init__(self, board):
        self.board = board

        self.candidates_by_priority_and_colour = []
        cbpc = self.candidates_by_priority_and_colour
        for priority in range(6):
            l = []
            cbpc.append(l)
            for colour in range(3):
                l.append({})

        self.tried = set()

    def get_iter(self, our_colour):
        other_colour = opposite_colour(our_colour)

        for length in range(5):
            priority = 5 - length
            cbpc = self.candidates_by_priority_and_colour
            for colour in (our_colour, other_colour):
                slot = cbpc[priority][colour]
                for pos, count in slot.iteritems():
                    if count > 0:
                        if not pos in self.tried:
                            self.tried.add(pos)
                            yield pos

        # BLACKs first move
        if len(self.tried) == 0:
            brd = self.board
            half_board = brd.get_size() / 2
            yield (half_board, half_board)
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

    def add_or_remove_capture(self, colour, pos, inc=1):
        # Valuing captures between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc

    def add_or_remove_threat(self, colour, pos, inc=1):
        # Valuing captures between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        slot[pos] = slot.setdefault(pos, 0) + inc
