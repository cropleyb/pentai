import random
import pdb

from defines import *

class OpeningsFilter(object):
    def __init__(self, openings_mgr, game):
        self.openings_mgr = openings_mgr
        self.game = game

    def get_iter(self, colour):
        m = self.get_a_good_move(self, self.game)
        yield m

    def get_a_good_move(self, game, colour):
        wins = 0
        losses = 0
        totals = []

        move_games = self.openings_mgr.get_move_games(game)
        #colour = game.to_move_colour()
        
        for mg in move_games:
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

