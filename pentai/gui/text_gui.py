
import string
from gui import *

class TextGui(Gui):
    def __init__(self, game):
        self.game = game
        self.board_chars = []
        self.col_names = string.ascii_letters.replace('i','')[:game.size()]
        padding = '  '
        horiz_grid = [padding]
        horiz_grid.extend(self.col_names)

        # Horizontal grid
        self.board_chars.append(horiz_grid)

        for r in range(game.size()):
            row = []
            # Vertical grid on the left
            row_num_str = "%2d" % (game.size()-r)
            row.append(row_num_str)

            # Create a row of empty places for the stones to go
            for j in range(game.size()):
                row.append(' ')
            self.board_chars.append(row)

        # Horizontal grid is repeated at the bottom
        self.board_chars.append(horiz_grid)

        # We must watch what happens to the logical board, and update accordingly
        game.current_state.add_observer(self)

    def after_set_occ(self, pos, colour):
        col_char = " BW"[colour]
        x, y = pos

        # first and last rows are the horizontal grid
        row = self.board_chars[self.game.size()-y]

        row[x+1] = col_char

    def board_to_string(self):
        ret = []
        for row in self.board_chars:
            ret.append(" ".join(row))
            ret.append("\n")
        return "".join(ret)

    def player_detail(self, player_num):
        ret = ""
        if self.game.to_move_colour() == player_num:
            ret = "* "
        ret = ret + self.game.get_player(player_num).p_name
        num_captured = self.game.get_captured(player_num)
        if not self.game.rules.can_capture_threes:
            num_captured /= 2
            captured = str(num_captured) + 'p'
        else:
            captured = str(num_captured)
        ret = ret + " (" + captured + ")"
        return ret

    def aux_to_string(self):
        return self.player_detail(P1) + " vs. " \
             + self.player_detail(P2) + "\n"

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
                return (col, row)
        except:
            pass
        off_board_msg = "That position is not on the board"
        raise IllegalMoveException(off_board_msg)
