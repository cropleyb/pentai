import random
import pdb

from defines import *

class OpeningsFilter(object):
    def __init__(self):
        self.move_games = None

    def set_move_games(self, mgs):
        self.move_games = mgs

    #def get_iter(self, colour): TODO

    def get_a_good_move(self, colour):
        wins = 0
        losses = 0
        totals = []
        
        for mg in self.move_games:
            move, games = mg
            for game in games:
                win_colour = game.winner()
                if win_colour == colour:
                    wins += 1
                else:
                    assert(win_colour == opposite_colour(colour))
                    losses += 1
            totals.append((move, wins, losses))

        total_score = 1 # For fall through to inner filter

        #pdb.set_trace()

        move_scores = []
        for move, wins, losses in totals:
            score = (wins or .2)/(losses or .2)
            move_scores.append((move, score))
            total_score += score
        
        rand_val = random.random() * total_score

        for move, score in move_scores:
            if score > rand_val:
                return move
            rand_val -= score

        # Fall through to inner filter
        return None

