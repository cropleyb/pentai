
from game_state import *

class Game():

    def __init__(self, rules, player1, player2):
        self.rules = rules
        self.player = [player1, player2]
        self.current_state = GameState(self)

    def size(self):
        return self.rules.size

    def get_player(self, player_number):
        return self.player[player_number]

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
        pass

