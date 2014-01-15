class OpeningsFilter(object):
    def __init__(self):
        self.move_games = None

    def set_move_games(self, mgs):
        self.move_games = mgs

    def get_iter(self, colour):
        if len(self.move_games) == 0:
            return

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
                    assert(win_colour == other_colour(colour))
                    losses += 1
            totals.append((move, wins, losses))

        scores = [(move, wins/(losses or 0.1)) for move, wins, losses in totals]

        scores.sort(reverse=True)
        
        yield scores[0][0]

