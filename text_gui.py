
import string
from gui import *

black = 1
white = 2

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

    def player_detail(self, player_num):
        ret = ""
        if self.game.get_move_number() % 2 != player_num:
            ret = "* "
        ret = ret + self.game.get_player(player_num).name
        num_captured = self.game.get_captured(player_num)
        if not self.game.rules.can_capture_threes:
            num_captured /= 2
            captured = str(num_captured) + 'p'
        else:
            captured = str(num_captured)
        ret = ret + " (" + captured + ")"
        return ret

    def aux_to_string(self):
        return self.player_detail(0) + " vs. " + self.player_detail(1) + "\n"

    def request_move(self, name):
        ret = [self.board_to_string()]
        ret.append(self.aux_to_string())
        ret.append("Your move, " + name + ":\n")
        return "".join(ret)

    def get_action(self):
        s = raw_input().strip()
        return self.get_action_from_string(s)

    def get_action_from_string(self, s):
        col = self.col_names.find(s[0]) + 1
        row = string.atoi(s[1:])
        if col < 0 or col >= self.game.size:
            raise IllegalMoveException()
        if row < 0 or row >= self.game.size:
            raise IllegalMoveException()
        return MoveAction(col, row)
