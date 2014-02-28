
# This is just be a base class / interface to be filled out by 
# human and AI players.

# TODO: Undo support?
# TODO: Resign?

class Player():
    def __init__(self, p_name):
        self.p_name = p_name
        self.remaining_time = 0

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

    def get_total_time(self):
        return self.total_time

    def tick(self, seconds):
        self.remaining_time -= seconds
        return self.remaining_time

    def set_remaining_time(self, t):
        self.remaining_time = t

    def prompt_for_action(self, game, gui):
        pass

    def get_action(self, game, gui):
        pass

    def rating_factor(self):
        return 1

    def attach_to_game(self, base_game):
        # TODO: Restore from history
        self.total_time = base_game.get_rules().time_control
        self.remaining_time = base_game.get_rules().time_control

