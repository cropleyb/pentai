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
                l.append(set())

        self.tried = set()

    def get_iter(self, our_colour):
        other_colour = opposite_colour(our_colour)

        for length in range(5):
            priority = 5 - length
            cbpc = self.candidates_by_priority_and_colour
            for colour in (our_colour, other_colour):
                for pos in cbpc[priority][colour]:
                    if not pos in self.tried:
                        self.tried.add(pos)
                        yield pos

        # BLACKs first move
        if len(self.tried) == 0:
            brd = self.board
            half_board = brd.get_size() / 2
            yield (half_board, half_board)
            return

    def add_or_remove_candidates(self, colour, length, pos_list, add=True):
        if length == 5:
            # won already, ignore
            return
        if length == 4: # allow space for capture priority
            length = 5
        if length < 3:  # allow space for threat priority
            length -= 1
        slot = self.candidates_by_priority_and_colour[length][colour]
        if add:
            slot.update(pos_list)
        else:
            slot.difference_update(pos_list)

    def add_or_remove_capture(self, colour, pos, add=True):
        # Valuing captures between 3s and 4s
        slot = self.candidates_by_priority_and_colour[4][colour]
        if add:
            slot.add(pos)
        else:
            slot.remove(pos)

    def add_or_remove_threat(self, colour, pos, add=True):
        # Valuing captures between 2s and 3s
        slot = self.candidates_by_priority_and_colour[2][colour]
        if add:
            slot.add(pos)
        else:
            slot.remove(pos)
