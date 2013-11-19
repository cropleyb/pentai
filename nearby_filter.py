from defines import *
from pente_exceptions import *

import pdb

def shift(move, d, dist):
    x, y = move
    new_pos = (x + (d[0] * dist), \
               y + (d[1] * dist)) 
    return new_pos


def add_successors(move, board, successors, min_dist, max_dist):
    dir_count = [0] * len(DIRECTIONS)
    for dist in range(min_dist, max_dist+1):
        for d_ind in range(len(DIRECTIONS)):
            d = DIRECTIONS[d_ind]
            succ_pos = shift(move, d, dist)
            try:
                if board.get_occ(succ_pos) == EMPTY:
                    if dir_count[d_ind] < 2:
                        successors.add(succ_pos)
                        dir_count[d_ind] += 1

            except OffBoardException:
                pass

class NearbyFilter():
    def __init__(self, board):
        self.board = board
        self.moves = []
        self.captures = []

    def clone(self):
        other = NearbyFilter(self.board)
        other.moves = self.moves[:]
        other.captures = self.captures[:]

    def get_iter(self):
        brd = self.board
        if len(self.moves) == 0:
            half_board = brd.get_size() / 2
            yield (half_board, half_board)
            return
        successors = set()
        all_captures = []
        for cs in self.captures:
            all_captures.extend(cs)

        for capture in all_captures:
            add_successors(capture, brd, successors, min_dist=0, max_dist=1)
        for move in self.moves:
            add_successors(move, brd, successors, min_dist=1, max_dist=5)

        for succ in successors:
            yield succ
            
    def move(self, pos):
        self.moves.append(pos)
        self.captures.append([])
        if len(self.moves) > 2:
            self.moves = self.moves[-2:]
        if len(self.captures) > 2:
            self.captures = self.captures[-2:]

    def capture(self, pos):
        self.captures[-1].append(pos)
