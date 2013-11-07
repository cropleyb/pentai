class IllegalMoveException(Exception):
    pass

from game import *

class MoveAction():
    @staticmethod 
    def create_from_move(move):
        return MoveAction(move)
    
    @staticmethod 
    def create_from_tuple(x, y):
        return MoveAction(Move(Pos(x, y)))

    def __init__(self, move):
        self.move = move

    def __eq__(self, other):
        return self.move == other.move

    def __repr__(self):
        return str(self.move)

    def perform(self, game):
        game.make_move(self.move)

class Gui():
    # TODO: base interface, constructor chaining takes (game)
    pass
