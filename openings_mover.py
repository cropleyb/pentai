import random
import pdb

from defines import *

class OpeningsMover(object):
    def __init__(self, o_mgr, game):
        self.o_mgr = o_mgr
        self.game = game

    def get_a_good_move(self):
        wins = 0
        losses = 0
        totals = []

        colour = self.game.to_move_colour()

        move_games = self.o_mgr.get_move_games(self.game)
        
        for mg in move_games:
            move, games = mg
            for g in games:
                win_colour = g.winner()

                if win_colour == colour:
                    wins += 1
                else:
                    assert(win_colour == opposite_colour(colour))
                    losses += 1
            totals.append((move, wins, losses))

        total_score = 1 # For fall through to inner filter

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

