import random

from pentai.base.defines import *
import pentai.base.logger as log

class OpeningsMover(object):
    def __init__(self, o_book, ab_game):
        self.o_book = o_book
        self.game = ab_game.get_base_game()

    def get_a_good_move(self, aip, seen=None, force=False):
        # TODO: shouldn't need to pass in aip each time, make it self.player?
        if seen is None:
            seen = set()

        search_colour = self.game.to_move_colour()
        other_colour = opposite_colour(search_colour)
        move_games = list(self.o_book.get_move_games(self.game))
        log.debug("move_games: %s", len(move_games))
        ri = random.randint(0,len(move_games))
        mg2 = move_games[ri:] + move_games[:ri]

        total_score = .1 # For fall through to default search
        if force:
            total_score = 0.0

        score_moves = []
        for move, data, secondary in mg2:
            if not self.game.is_live():
                log.info("Interrupted opening book search")
                return

            # Note that duplicate moves are possible from the different rules.
            seen.add(move)

            # TODO: Store scores in the DB? retain flexibility for now
            mr_factor = data.get_max_rating() / 1000.0
            wins = float(data.get_wins(search_colour))
            losses = data.get_wins(other_colour)
            if wins/(losses+wins) < .4:
                continue
            score = (mr_factor * (wins or .3))/(losses or .2)

            if secondary:
                # Moves from games with different rules are not likely to be
                # as good
                score *= .01

            score_moves.append((score, move))
            total_score += score

        score_moves.sort(reverse=True)

        rand_val = random.random() * total_score

        for score, move in score_moves:
            log.debug("score: %s, rand_val: %s" % (score, rand_val))
            if score >= rand_val:
                log.debug("Chose %s, score: %s (out of %s)" % (move, score, total_score))
                return move
            rand_val -= score

        # Fall through to inner filter
        if len(score_moves) > 0:
            log.info("Fall through despite opening option(s) %s" % total_score)
        else:
            log.info("No suitable opening options found")
        return None


