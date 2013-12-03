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
            for pos in cbpc[priority][our_colour]:
                if not pos in self.tried:
                    self.tried.add(pos)
                    yield pos
            for pos in cbpc[priority][other_colour]:
                if not pos in self.tried:
                    self.tried.add(pos)
                    yield pos
                # Ignore duplicates

        # BLACKs first move
        if len(self.tried) == 0:
            brd = self.board
            half_board = brd.get_size() / 2
            yield (half_board, half_board)
            return

    def report_candidates(self, colour, length, pos_list):
        if length == 5:
            # won already, ignore
            return
        if length == 4:
            length = 5
        self.candidates_by_priority_and_colour[length][colour].update(pos_list)

    def report_capture(self, colour, pos):
        # HACK - I am valuing captures between 3s and 4s
        self.candidates_by_priority_and_colour[4][colour].add(pos)
