
# TODO: This should just be a base class / interface to be filled out by 
# human and AI players.

class Player():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

