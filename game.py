
from game_state import *

class Move():
    def __init__(self, pos):
        self.pos = pos

    def position(self):
        return self.pos

    def __eq__(self, other):
        return self.pos == other.pos

class Game():

    def __init__(self, rules, player1, player2):
        self.rules = rules
        self.player = [player1, player2]
        self.current_state = GameState(self)

    def size(self):
        return self.rules.size

    def get_player(self, player_number):
        return self.player[player_number]

    def get_current_player(self):
        return self.player[self.current_state.to_move()]

    def prompt_for_action(self, gui):
        return self.get_current_player().prompt_for_action(gui)

    def get_action(self, gui):
        return self.get_current_player().get_action(gui)

    # Not sure if these should even delegate
    def get_move_number(self):
        return self.current_state.get_move_number()

    def set_move_number(self, turn):
        self.current_state.set_move_number(turn)

    def get_captured(self, player_number):
        return self.current_state.get_captured(player_number)

    def set_captured(self, player_number, pieces):
        return self.current_state.set_captured(player_number, pieces)

    def make_move(self, move):
        self.current_state.make_move(move)

    def finished(self):
        return self.current_state.get_won_by() > 0

    def winner(self):
        return self.current_state.get_won_by()

    def winner_name(self):
        return self.player[self.current_state.get_won_by()]

