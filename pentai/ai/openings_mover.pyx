import random

from pentai.base.defines import *

class OpeningsMover(object):
    def __init__(self, o_book, ab_game):
        self.o_book = o_book
        self.game = ab_game.get_base_game()

    def get_a_good_move_new(self, aip, seen=None):
        # TODO: shouldn't need to pass in aip each time, make it self.player?

        if seen is None:
            seen = set()

        search_colour = self.game.to_move_colour()
        other_colour = opposite_colour(search_colour)
        move_games = self.o_book.get_move_games(self.game)

        total_score = .1 # For fall through to default search

        move_scores = []
        for move, data in move_games:
            if not self.game.is_live():
                log.info("Interrupted opening book search")
                return
            seen.add(move)

            # TODO: Store scores in the DB? retain flexibility for now
            mr_factor = data.get_max_rating() / 1000.0
            wins = data.get_wins(search_colour)
            losses = data.get_wins(other_colour)
            score = (mr_factor * (wins or .3))/(losses or .2)

            move_scores.append((move, score))
            total_score += score
        
        rand_val = random.random() * total_score

        for move, score in move_scores:
            log.debug("score: %s, rand_val: %s" % (score, rand_val))
            if score >= rand_val:
                log.debug("Chosen score: %s (out of %s)" % (score, total_score))
                return move
            rand_val -= score

        # Fall through to inner filter
        if len(move_scores) > 0:
            log.info("Fall through despite opening option(s) %s" % total_score)
        else:
            log.info("No suitable opening options found")
        return None

    def get_a_good_move(self, aip, seen=None):
        # TODO: shouldn't need to pass in aip each time, make it self.player?
        wins = 0
        losses = 0
        totals = []

        if seen is None:
            seen = set()

        colour = self.game.to_move_colour()

        max_rating = .1

        move_games = self.o_book.get_move_games(self.game)

        for mg in move_games:
            if not self.game.is_live():
                log.info("Interrupted opening book search")
                return
            move, games = mg
            for pg in games:

                win_colour = pg.won_by

                if win_colour == colour:
                    wins += 1
                elif win_colour == opposite_colour(colour):
                    losses += 1
                # count draws and unfinished games as no win, no loss

                move_rating = pg.get_rating(colour)
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
            log.debug("score: %s, rand_val: %s" % (score, rand_val))
            if score >= rand_val:
                log.debug("Chosen score: %s (out of %s)" % (score, total_score))
                return move
            rand_val -= score

        # Fall through to inner filter
        if len(totals) > 0:
            log.info("Fall through despite opening option(s) %s" % total_score)
        else:
            log.info("No suitable opening options found")
        return None

