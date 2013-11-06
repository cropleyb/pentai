
from game_state import *

class Game():

    def __init__(self, rules, player1, player2):
        self.rules = rules
        self.player = [player1, player2]
        self.current_state = GameState(self)
        # TODO: I think these belong in board - dynamic game state
        self.move_number = 0
        self.captures = [0, 0]

    def size(self):
        return self.rules.size

    def get_player(self, player_number):
        return self.player[player_number]

    def get_move_number(self):
        return self.move_number

    def get_captures(self, player_number):
        return self.captures[player_number]

    def make_move(self, move):
        pass

