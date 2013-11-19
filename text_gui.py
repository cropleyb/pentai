
import string
from gui import *

empty = 0
black = 1
white = 2

class TextGui(Gui):
    def __init__(self, game):
        self.game = game
        self.board_chars = []
        self.col_names = string.ascii_letters.replace('i','')[:game.size()]
        padding = '  '
        first_row = [padding]
        first_row.extend(self.col_names)
        self.board_chars.append(first_row)
        for i in range(game.size()):
            row = []
            self.board_chars.append(row)
            row_num_str = "%2d" % (game.size()-i)
            row.append(row_num_str)
            for j in range(game.size() - 1):
                row.append(' ')
        self.board_chars.append(first_row)

        # We must watch what happens to the logical board, and update accordingly
        board = game.current_state.board
        board.add_observer(self)

    def after_set_occ(self, pos, colour):
        if colour == 1:
            col_char = "B"
        elif colour == 2:
            col_char = "W"
        else:
            col_char = " "
        x = pos[0]
        y = pos[1]
        self.board_chars[self.game.size()-y][x+1] = col_char

    def board_to_string(self):
        ret = []
        for row in self.board_chars:
            #row = row[:-1]
            ret.append(" ".join(row))
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
        try:
            col = self.col_names.find(s[0])
            row = string.atoi(s[1:]) - 1
            if col >= 0 and col < self.game.size() and \
               row >= 0 and row < self.game.size():
                return MoveAction.create_from_tuple(col, row)
        except:
            pass
        off_board_msg = "That position is not on the board"
        raise IllegalMoveException(off_board_msg)
