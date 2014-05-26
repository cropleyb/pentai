
from persistent import *

from pentai.base.defines import *

class OpeningMoveData(Persistent):
    def __init__(self):
        self.b_wins = 0
        self.w_wins = 0
        self.total_rating = 0
        self.max_rating = 0

    def get_wins(self, colour):
        if colour == BLACK:
            return self.b_wins
        else:
            return self.w_wins

    def get_avg_rating(self):
        return int(float(self.total_rating) / (self.b_wins + self.w_wins))

    def get_max_rating(self):
        return self.max_rating

    def add_game(self, colour, rating):
        if colour == BLACK:
            self.b_wins += 1
        else:
            self.w_wins += 1
        self.total_rating += rating
        if self.max_rating < rating:
            self.max_rating = rating

class OpeningPosData(Persistent):
    def __init__(self):
        self.moves = {} # TODO PD

    def get_moves(self):
        return self.moves

    def add_move(self, pos, *args):
        omd = self.moves.setdefault(pos, OpeningMoveData())
        omd.add_game(*args)

