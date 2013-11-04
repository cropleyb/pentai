
import string

black = 1
white = 2

class TextGui():
    def __init__(self, game):
        self.game = game
        self.board_chars = []
        first_row = [' ']
        first_row.extend([string.ascii_letters[j] for j in range(game.size())])
        self.board_chars.append(first_row)
        for i in range(game.size()):
            row = []
            self.board_chars.append(row)
            row.append(str(game.size()-i))
            for j in range(game.size()):
                row.append(' ')

    def place_stone(self, x, y, colour):
        if colour == 1:
            col_char = "B"
        elif colour == 2:
            col_char = "W"
        self.board_chars[1+self.game.size()-y][x] = col_char

    def remove_stone(self, x, y):
        self.board_chars[1+self.game.size()-y][x] = " "

    def board_to_string(self):
        ret = []
        for r in self.board_chars:
            ret.append("".join(r))
            ret.append("\n")
        return "".join(ret)
'''
- Place stone (pos, colour)
- Remove stone (pos)
- add captured stone
- remove captured stone (for undo/rewind)
- draw board / flush() (pass for Kivy)
  - show who is to move (though this isn't a method of the class)
- get a move
'''
