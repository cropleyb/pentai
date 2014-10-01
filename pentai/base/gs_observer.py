
class GSObserver(object):
    def before_set_occ(self, game, pos, colour):
        pass

    def after_set_occ(self, game, pos, colour):
        pass

    def up_to_date(self, game):
        pass

    def after_game_won(self, game, colour):
        pass
