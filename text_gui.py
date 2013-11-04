
black = 1
white = 2

class TextGui():
    def __init__(self, game):
        self.game = game

    def place_stone(self, x, y, colour):
        pass

    def to_string(self):
        return ""
'''
- Place stone (pos, colour)
- Remove stone (pos)
- add captured stone
- remove captured stone (for undo/rewind)
- draw board / flush() (pass for Kivy)
  - show who is to move (though this isn't a method of the class)
- get a move
'''
