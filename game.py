

class Game():

    def __init__(self, rules, player1, player2):
        self.rules = rules
        self.player = [player1, player2]
        self.move_number = 0

    def size(self):
        return self.rules.size

    def get_player(self, player_number):
        return self.player[player_number]

    def get_move_number(self):
        return self.move_number
