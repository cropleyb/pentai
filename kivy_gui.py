from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.graphics import *

from gui import *

black_filename = "./images/black_transparent.png"
white_filename = "./images/white_transparent.png"
x_filename = "./images/X_transparent.png"

class BoardWidget(Widget):
    source = StringProperty(None)

    def __init__(self, *args, **kwargs):
        self.marker = None
        self.move_number = 0

        self.stones_by_board_pos = {}
        super(BoardWidget, self).__init__(*args, **kwargs)

    def set_game(self, game):
        self.game = game

        # We must watch what happens to the logical board, and update accordingly
        board = game.get_board()
        board.add_observer(self)

    def board_size(self):
        return self.game.size()

    def grid_size(self):
        ''' The Grid on the screen allows extra space at the edges '''
        return self.game.size() + 1

    def after_set_occ(self, pos, colour):
        # TODO look up self.stones_by_board_pos.
        # If it is unoccupied, create a piece of the appropriate colour.
        # If it is occupied, remove it.
        self.make_move_on_the_board(pos, colour)

    def set_up_grid(self, _dt):
        """ Create black grid lines """
        size_x = self.size[0]
        size_y = self.size[1]

        with self.canvas:
            Color(0, 0, 0)
            grid_size_x = float(size_x) / (self.grid_size())
            grid_size_y = float(size_y) / (self.grid_size())
            GS = self.grid_size()
            # horizontal lines
            for y in range(1,GS):
                Rectangle(pos=(grid_size_x-1, grid_size_y*y-1), \
                          size=(grid_size_x * (self.grid_size()-2), 3))
            # vertical lines
            for x in range(1,GS):
                Rectangle(pos=(grid_size_x*x-1, grid_size_y-1), \
                          size=(3, grid_size_y * (self.grid_size()-2)))

    def snap_to_grid(self, screen_pos):
        return self.board_to_screen(self.screen_to_board(screen_pos))

    def screen_to_board(self, screen_pos):
        """ Convert a screen position (in pixels) to a board coordinate pair,
            dependant on the size of the board """
        size_x, size_y = self.size
        GS = self.grid_size()
        board_x = round(GS * screen_pos[0] / size_x) - 1
        board_y = round(GS * screen_pos[1] / size_y) - 1
        return board_x, board_y

    def board_to_screen(self, board_pos):
        """ Convert a board coordinate pair to a screen position (in pixels),
            dependant on the size of the board """
        size_x, size_y = self.size
        GS = self.grid_size()
        screen_x = ((board_pos[0] + 1) / GS) * size_x
        screen_y = ((board_pos[1] + 1) / GS) * size_y
        return screen_x, screen_y

    def on_touch_down(self, touch):
        # Place a marker at the (snapped) cursor position.
        if self.marker == None:
            try:
                # load the image
                # TODO: Separate class?
                self.marker = Piece(source=x_filename)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % x_filename)
        self.marker.pos = self.snap_to_grid(touch.pos)
        self.add_widget(self.marker)

    def on_touch_up(self, touch):
        # If there is an active marker:
        # Replace the marker to a piece of the appropriate colour
        # TODO: make the move with the appropriate board position
        # TODO: Check that it is a human's turn.
        if self.marker != None:
            self.remove_widget(self.marker)
            # Quick hack to get both coloured stones on the board
            board_pos = self.screen_to_board(touch.pos)

            # TODO: use game, board, check for off board, illegal move exceptions
            # TEMP HACK
            to_move = (self.move_number + 1) % 2
            colour = to_move + 1

            self.make_move_on_the_board(board_pos, colour)

    def make_move_on_the_board(self, board_pos, colour): # TODO: Colour
        if self.stones_by_board_pos.has_key(board_pos) or colour == EMPTY:
            # There is a piece there already, remove it.
            assert colour == EMPTY
            current_piece = self.stones_by_board_pos[board_pos]
            self.remove_widget(current_piece)
        else:
            # Nothing there yet, place a stone
            filename = ["", white_filename, black_filename][colour]

            # TEMP HACK
            self.move_number += 1
            try:
                # load the image
                new_piece = Piece(source=filename)
                self.stones_by_board_pos[board_pos] = new_piece
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)

    def on_touch_move(self, touch):
        # TODO: Check for off board, remove marker
        if self.marker != None:
            # Move the marker position
            self.marker.pos = self.snap_to_grid(touch.pos)

class Piece(Scatter):
    source = StringProperty(None)

'''
class KivyGui(Gui):
    def __init__(self, game):
        self.game = game

        # We must watch what happens to the logical board, and update accordingly
        board = game.current_state.board
        board.add_observer(self)

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
'''
