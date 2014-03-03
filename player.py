
# This is just be a base class / interface to be filled out by 
# human and AI players.

# TODO: Undo support?
# TODO: Resign?

# super requires inheriting from object, which clashes with pickle?!
#class Player(object):
class Player():
    def __init__(self, p_name):
        self.p_name = p_name

    def __repr__(self):
        return self.p_name

    def get_type(self):
        return "BasePlayer"

    def get_key(self):
        return self.p_key

    def get_name(self):
        try:
            name = self.p_name
        except AttributeError:
            name = self.name
            self.p_name = name
            del self.name
        return name

    def prompt_for_action(self, game, gui):
        pass

    def get_action(self, game, gui):
        pass

    def rating_factor(self):
        return 1

    def attach_to_game(self, base_game):
        pass

