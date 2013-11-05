
import string

black = 1
white = 2


class MoveAction():
    def __init__(self, move):
        self.move = move

class TextGui():
    def __init__(self, game):
        self.game = game
        self.board_chars = []
        self.col_names = string.ascii_letters.replace('i','')[:game.size()]
        padding = '   '
        first_row = [padding]
        first_row.extend(self.col_names)
        self.board_chars.append(first_row)
        for i in range(game.size()):
            row = []
            self.board_chars.append(row)
            row_num_str = "%2d " % (game.size()-i)
            row.append(row_num_str)
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

    # def set_who_is_to_move(self, player)

    def aux_to_string(self):
        p1 = self.game.get_player(0).name
        p2 = self.game.get_player(1).name
        if self.game.get_move_number() % 2 == 0:
            p1 = "* " + p1
        else:
            p2 = "* " + p2
        return p1 + " vs. " + p2 + "\n"

    def request_move(self, name):
        ret = [self.board_to_string()]
        ret.append(self.aux_to_string())
        ret.append("Your move, " + name + ":\n")
        return "".join(ret)

    def get_action(self):
        return self.gui.get_action()
