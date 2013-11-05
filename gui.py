class IllegalMoveException(Exception):
    pass

class MoveAction():
    def __init__(self, x, y):
        self.move = (x, y) 

    def __eq__(self, other):
        return self.move == other.move

    def __repr__(self):
        return str(self.move)

class Gui():
    pass
