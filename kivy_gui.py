from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics import *

from gui import *

import Queue

black_filename = "./images/black_transparent.png"
white_filename = "./images/white_transparent.png"
x_filename = "./images/X_transparent.png"

import pdb

class BoardWidget(Widget):
    source = StringProperty(None)

    def __init__(self, *args, **kwargs):
        self.marker = None
        self.stones_by_board_pos = {}
        self.action_queue = Queue.Queue()

        super(BoardWidget, self).__init__(*args, **kwargs)

    def set_game(self, game):
        self.game = game

        # We must watch what happens to the logical board, and update accordingly
        board = game.get_board()
        board.add_observer(self)

        self.trig = Clock.create_trigger(self.perform)

        # start the game
        prompt = game.prompt_for_action(self)
        self.display_feedback_string(prompt)

    def display_feedback_string(self, message):
        # TODO: Update screen
        print message

    def request_move(self, name):
        # TODO: Update side panel instead, use player object param instead of name
        your_move = "Your move, %s" % name
        return your_move

    def enqueue_action(self, action):
        self.action_queue.put(action)
        self.trig()

    def perform(self, dt):
        if self.action_queue.empty():
            return
        action = self.action_queue.get()
        action.perform(self.game)
        prompt = self.game.prompt_for_action(self)
        self.display_feedback_string(prompt)

    def board_size(self):
        return self.game.size()

    def grid_size(self):
        """ The Grid on the screen allows extra space at the edges """
        return self.game.size() + 1

    def before_set_occ(self, pos, colour):
        pass

    def after_set_occ(self, pos, colour):
        self.make_move_on_the_gui_board(pos, colour)

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
        board_x = int(round(GS * screen_pos[0] / size_x) - 1)
        board_y = int(round(GS * screen_pos[1] / size_y) - 1)
        return board_x, board_y

    def board_to_screen(self, board_pos):
        """ Convert a board coordinate pair to a screen position (in pixels),
            dependant on the size of the board """
        size_x, size_y = self.size

        # Use float() to avoid python int / int = int prob
        GS = float(self.grid_size())
        screen_x = ((board_pos[0] + 1) / GS) * size_x
        screen_y = ((board_pos[1] + 1) / GS) * size_y
        return screen_x, screen_y

    def on_touch_down(self, touch):
        # Check that it is a human's turn.
        current_player = self.game.get_current_player()
        if current_player.get_type() == "human":
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
        else:
            self.display_feedback_string("It is not your turn!")

    def on_touch_up(self, touch):
        # If there is an active marker,
        # replace the marker with a piece of the appropriate colour
        if self.marker != None:
            self.remove_widget(self.marker)
            self.marker = None
            # Quick hack to get both coloured stones on the board
            board_pos = self.screen_to_board(touch.pos)

            # Make and Queue MoveAction
            ma = MoveAction.create_from_move(board_pos)
            self.enqueue_action(ma)

    def make_move_on_the_gui_board(self, board_pos, colour):
        if self.stones_by_board_pos.has_key(board_pos) or colour == EMPTY:
            # There is a piece there already, remove it.
            assert colour == EMPTY
            current_piece = self.stones_by_board_pos.pop(board_pos)
            self.remove_widget(current_piece)
        else:
            # Nothing there yet, place a stone
            filename = ["", black_filename, white_filename][colour]

            try:
                # load the image
                new_piece = Piece(source=filename)
                self.stones_by_board_pos[board_pos] = new_piece
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)

    def on_touch_move(self, touch):
        # TODO: Check for off board? remove marker?
        if self.marker != None:
            # Move the marker position
            self.marker.pos = self.snap_to_grid(touch.pos)

class Piece(Scatter):
    source = StringProperty(None)

