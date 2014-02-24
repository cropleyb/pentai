import random
import pdb
import time # TEMP

from defines import *

class OpeningsMover(object):
    def __init__(self, o_mgr, game):
        self.o_mgr = o_mgr
        self.game = game

    def get_a_good_move(self):
        print "Searching openings book"
        start = time.time()

        wins = 0
        losses = 0
        totals = []

        colour = self.game.to_move_colour()
        max_rating_factor = 1

        move_games = self.o_mgr.get_move_games(self.game)
        
        for mg in move_games:
            move, games = mg
            for g in games:
                win_colour = g.get_won_by()

                if win_colour == colour:
                    wins += 1
                else:
                    assert(win_colour == opposite_colour(colour))
                    losses += 1

                # Calc & save the maximum rating of the players
                # who made this move
                move_player = g.get_player(colour)

                if move_player:
                    max_rating_factor = \
                        max(max_rating_factor, move_player.rating_factor())

            totals.append((move, wins, losses, max_rating_factor))

        total_score = 1 # For fall through to inner filter

        move_scores = []
        for move, wins, losses, mrf in totals:
            score = (mrf * (wins or .2))/(losses or .2)
            move_scores.append((move, score))
            total_score += score
        
        rand_val = random.random() * total_score

        for move, score in move_scores:
            if score > rand_val:
                end = time.time()
                diff = end - start
                print "Move found in %s" % diff
                return move
            rand_val -= score

        print "No move found"
        # Fall through to inner filter
        return None

