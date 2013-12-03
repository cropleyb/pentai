from defines import *

class PriorityFilter():
    def __init__(self, board):
        self.board = board

        self.candidates_by_colour_and_priority = []
        for colour in range(4):
            cbcp = self.candidates_by_colour_and_priority
            l = []
            cbcp.append(l)
            for priority in range(6):
                l.append(set())

        self.tried = set()

    def get_iter(self, our_colour):
        other_colour = opposite_colour(our_colour)

        for length in range(5):
            priority = 5 - length
            cbcp = self.candidates_by_colour_and_priority
            for pos in cbcp[our_colour][priority]:
                if not pos in self.tried:
                    self.tried.add(pos)
                    yield pos
            for pos in cbcp[other_colour][priority]:
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
        self.candidates_by_colour_and_priority[colour][length].update(pos_list)
