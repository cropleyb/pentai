import random

from pentai.base.defines import *

class OpeningsMover(object):
    def __init__(self, o_book, game):
        self.o_book = o_book
        self.game = game

    def filter_out_by_rules(self, move):
        rules = self.game.get_rules()
        return rules.ok_third_move(move)

    def get_a_good_move(self, aip, seen=None):
        # TODO: shouldn't need to pass in aip each time, make it self.player?
        wins = 0
        losses = 0
        totals = []

        if seen is None:
            seen = set()

        colour = self.game.to_move_colour()
        move_number = self.game.get_move_number()

        max_rating = .1

        move_games = self.o_book.get_move_games(self.game)

        ai_rating = aip.get_rating()
        
        for mg in move_games:
            move, games = mg
            if move_number == 3:
                if self.filter_out_by_rules(move):
                    continue
            for pg in games:

                move_rating = pg.get_rating(colour)
                if move_rating < (ai_rating + 300):
                    print "Move rating too low"
                    continue
                
                win_colour = pg.won_by

                if win_colour == colour:
                    wins += 1
                elif win_colour == opposite_colour(colour):
                    losses += 1
                else:
                    # ignore draws and unfinished games (latter shouldn't get here)
                    print "Game drawn or unfinished?"
                    continue

                # TODO: More smarts here
                max_rating = max(max_rating, move_rating)

            if max_rating >= 1:
                totals.append((move, wins, losses, max_rating))

        total_score = .1 # For fall through to inner filter

        move_scores = []
        for move, wins, losses, mr in totals:
            seen.add(move)
            mr_factor = mr / 1000.0
            score = (mr_factor * (wins))/(losses or .2)
            move_scores.append((move, score))
            total_score += score
        
        rand_val = random.random() * total_score

        for move, score in move_scores:
            #print "score: %s, rand_val: %s" % (score, rand_val)
            if score >= rand_val:
                print "Chosen score: %s (out of %s)" % (score, total_score)
                return move
            rand_val -= score

        # Fall through to inner filter
        if len(totals) > 0:
            print "Fall through despite opening option(s) %s" % total_score
        else:
            print "No options found"
        return None

