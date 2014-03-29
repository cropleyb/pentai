import random
import pdb

from defines import *

class OpeningsMover(object):
    def __init__(self, o_book, game):
        self.o_book = o_book
        self.game = game

    def get_a_good_move(self, aip):
        wins = 0
        losses = 0
        totals = []

        colour = self.game.to_move_colour()

        max_rating_factor = .1

        move_games = self.o_book.get_move_games(self.game)

        ai_rating = aip.get_rating()
        
        for mg in move_games:
            move, games = mg
            for pg in games:

                move_rating = pg.get_rating(colour)
                if move_rating < ai_rating:
                    continue

                win_colour = pg.won_by

                if win_colour == colour:
                    wins += 1
                elif win_colour == opposite_colour(colour):
                    losses += 1
                # else ignore draws and unfinished games (latter shouldn't get here)

                # TODO: More smarts here
                max_rating_factor = \
                    max(max_rating_factor, move_rating)

            if max_rating_factor >= 1:
                totals.append((move, wins, losses, max_rating_factor))

        total_score = 1 # For fall through to inner filter

        move_scores = []
        for move, wins, losses, mrf in totals:
            score = (mrf * (wins))/(losses or .2)
            move_scores.append((move, score))
            total_score += score
        
        rand_val = random.random() * total_score

        for move, score in move_scores:
            if score > rand_val:
                return move
            rand_val -= score

        # Fall through to inner filter
        return None

