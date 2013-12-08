from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import *
#from kivy.core.audio import SoundLoader TODO

from defines import *
from gui import *

import Queue

black_filename = "./media/black_transparent.png"
white_filename = "./media/white_transparent.png"
black_ghost_filename = "./media/black_ghost.png"
white_ghost_filename = "./media/white_ghost.png"
x_filename = "./media/X_transparent.png"
moved_marker_filename_w = "./media/moved_marker_w.png"
moved_marker_filename_b = "./media/moved_marker_b.png"
stone_sound = "./media/click.mp3"

class PenteScreen(Screen):
    source = StringProperty(None)
    # TODO: Get the times hooked up
    black_name = StringProperty("Freddo")
    white_name = StringProperty("Deep Thunk")
    black_time = StringProperty("0:00")
    white_time = StringProperty("0:00")
    black_to_move_marker = StringProperty("*")
    white_to_move_marker = StringProperty("")
    black_captures = StringProperty("0")
    white_captures = StringProperty("0")
    gridlines = ListProperty([])
    border_lines = ListProperty([0,0,0,0])
    border_colour = ListProperty([20,0,0,1])
    # TODO: Only the vertical offset is used so far.
    board_offset = ListProperty([0,80.0])

    def __init__(self, *args, **kwargs):
        self.marker = None
        self.stones_by_board_pos = {}
        self.action_queue = Queue.Queue()
        self.moved_marker = [None, None, None]
        self.ghosts = []
        self.ghost_colour = None
        self.queued_filename = ""
        #self.queued_filename = "./games/sample.txt"

        super(PenteScreen, self).__init__(*args, **kwargs)

    def set_game(self, game):
        self.game = game

        # We must watch what happens to the logical board, and update accordingly
        board = game.get_board()
        board.add_observer(self)

        self.trig = Clock.create_trigger(self.perform)
        self.set_up_grid()

        self.black_name = game.get_player_name(BLACK)
        self.white_name = game.get_player_name(WHITE)

        if len(self.queued_filename) > 0:
            # Need some time for kivy to finish setting up, otherwise
            # the pieces are all stacked in the bottom left corner.
            Clock.schedule_once(self.load_file, 0)

        # start the game
        game.prompt_for_action(self)


    def display_error(self, message):
        # TODO: Update screen
        # TODO: Enter to close
        popup = Popup(title='Error', content=Label(text=message, font_size='25sp'), \
                size_hint=(.7, .2))
        popup.open()
        print message

    def request_move(self, name):
        # TODO: Remove need for this - compat with Text GUI
        return ""

    def enqueue_action(self, action):
        self.action_queue.put(action)
        self.trig()

    def load_file(self, dt):
        f = open(self.queued_filename)
        # TODO: game info - players, rules etc.
        self.game.load_game(f.read())
        self.queued_filename = None

    def perform(self, dt):
        if self.action_queue.empty():
            return
        action = self.action_queue.get()
        try:
            self.game.make_move(action)
            self.update_captures_and_winner()
            self.game.prompt_for_action(self)
        except IllegalMoveException, e:
            self.display_error(e.message)

    def board_size(self):
        return self.game.size()

    def grid_size(self):
        """ The Grid on the screen allows extra space at the edges """
        return self.game.size() + 1

    def before_set_occ(self, pos, colour):
        pass

    def after_set_occ(self, pos, colour):
        self.make_move_on_the_gui_board(pos, colour)
        self.update_captures_and_winner()

    def play_sound(self):
        self.sound = SoundLoader.load(stone_sound)
        if self.sound:
            print("Sound found at %s" % self.sound.source)
            print("Sound is %.3f seconds" % self.sound.length)
        self.sound.play()

    def update_captures_and_winner(self):
        """ Update fields in the panel from changes to the game state """
        self.black_captures = str(self.game.get_captured(BLACK))
        self.white_captures = str(self.game.get_captured(WHITE))

        if self.game.finished():
            winner = self.game.winner()
            if winner == BLACK:
                self.black_to_move_marker = "won by"
                self.white_to_move_marker = ""
            elif winner == WHITE:
                self.black_to_move_marker = ""
                self.white_to_move_marker = "won by"
            # TODO draws are exceedingly unlikely...
        else:
            # Mark who is to move. TODO: Underline?
            to_move = self.game.to_move_colour()
            if to_move == BLACK:
                self.black_to_move_marker = "*"
                self.white_to_move_marker = ""
            elif to_move == WHITE:
                self.black_to_move_marker = ""
                self.white_to_move_marker = "*"

    def setup_grid_lines(self):
        size_x, size_y = self.size
        # Adjust for the position of the board being shifted so we can have a panel of
        # extra information.
        size_y -= self.board_offset[1]

        lines = []

        # This part is using the relative layout to get the lines in the right place
        # RL does not scale though.
        Color(0, 0, 0) # Black lines
        grid_size_x = float(size_x) / (self.grid_size())
        grid_size_y = float(size_y) / (self.grid_size())
        GS = self.grid_size()
        # horizontal lines
        for y in range(1,GS):
            # Each line is drawn twice, in opposite directions so we don't
            # get diagonal lines drawn as well
            this_end = (grid_size_x, grid_size_y*y)
            lines.extend(this_end)
            lines.extend((size_x-grid_size_x, grid_size_y*y))
            lines.extend(this_end)
        # vertical lines
        for x in range(1,GS):
            this_end = (grid_size_x*x, grid_size_y)
            lines.extend(this_end)
            lines.extend((grid_size_x*x, size_y-grid_size_y))
            lines.extend(this_end)
        self.setup_colour_border(size_x, size_y)
        return lines

    def setup_colour_border(self, size_x, size_y):
        w = 10
        # This is ugly, but using the "rectangle" feature causes issues in the corners
        self.border_lines = [0,w, size_x,w, w,w, w,size_y, 0,size_y-w, size_x,size_y-w]
        self.border_lines.extend([size_x-w,size_y, size_x-w,w])
        self.border_colour = self.game.rules.border_colour

    def set_up_grid(self, _dt=None):
        if hasattr(self, "game"):
            self.gridlines = self.setup_grid_lines()

    def snap_to_grid(self, screen_pos):
        return self.board_to_screen(self.screen_to_board(screen_pos))

    # screen_to_board and board_to_screen do their own compensating for
    # the canvas coordinate system covering the whole screen. It would be nice
    # if the RelativeLayout handled this. So far only the vertical axis has been
    # affected.
    def screen_to_board(self, screen_pos):
        """ Convert a screen position (in pixels) to a board coordinate pair,
            dependant on the size of the board """
        size_x, size_y = self.size
        bsp = screen_pos[0], screen_pos[1]-self.board_offset[1]
        size_y -= self.board_offset[1]
        GS = self.grid_size()
        board_x = int(round(GS * bsp[0] / size_x) - 1)
        board_y = int(round(GS * bsp[1] / size_y) - 1)
        if self.game.off_board((board_x, board_y)):
            raise IllegalMoveException
        return board_x, board_y

    def board_to_screen(self, board_pos):
        """ Convert a board coordinate pair to a screen position (in pixels),
            dependant on the size of the board """
        size_x, size_y = self.size
        size_y -= self.board_offset[1]

        # Use float() to avoid python int / int = int prob
        GS = float(self.grid_size())
        screen_x = ((board_pos[0] + 1) / GS) * size_x
        screen_y = ((board_pos[1] + 1) / GS) * size_y
        screen_y += self.board_offset[1]
        return screen_x, screen_y

    def update_moved_marker(self, pos, colour):
        filename = moved_marker_filename_w
        if colour == BLACK:
            filename = moved_marker_filename_b
        mm = self.moved_marker[colour]
        if mm == None:
            try:
                mm = Piece(self.game, source=filename)
                self.moved_marker[colour] = mm
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
                return
        else:
            self.remove_widget(mm)
        mm.pos = pos
        self.add_widget(mm)

    def on_touch_down(self, touch):
        # Check that it is a human's turn.
        current_player = self.game.get_current_player()
        if current_player.get_type() == "human":
            # Place a marker at the (snapped) cursor position.
            if self.marker == None:
                try:
                    # load the image
                    self.marker = Piece(self.game, source=x_filename)
                except Exception, e:
                    Logger.exception('Board: Unable to load <%s>' % x_filename)
            self.marker.pos = self.snap_to_grid(touch.pos)
            self.add_widget(self.marker)
        else:
            self.display_error("It is not your turn!")

    def on_touch_up(self, touch):
        # If there is an active marker,
        # replace the marker with a piece of the appropriate colour
        if self.marker != None:
            self.remove_widget(self.marker)
            self.marker = None
            # Quick hack to get both coloured stones on the board
            board_pos = self.screen_to_board(touch.pos)

            # Make and Queue
            ma = board_pos
            self.enqueue_action(ma)

    def remove_ghosts(self):
        while len(self.ghosts) > 0:
            g = self.ghosts.pop()
            self.remove_widget(g)

    def place_ghost(self, board_pos, colour):
        if colour != self.ghost_colour:
            self.remove_ghosts()
        filename = ["", black_ghost_filename, white_ghost_filename][colour]
        self.ghost_colour = colour

        try:
            # load and place the appropriate stone image
            new_piece = Piece(self.game, source=filename)
            new_piece.pos = self.board_to_screen(board_pos)
            self.ghosts.append(new_piece)
            self.add_widget(new_piece)
        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % filename)

    def make_move_on_the_gui_board(self, board_pos, colour):
        if colour == self.ghost_colour:
            self.remove_ghosts()
        if self.stones_by_board_pos.has_key(board_pos) or colour == EMPTY:
            # There is a piece there already, remove it.
            assert colour == EMPTY
            curr_piece, curr_colour = self.stones_by_board_pos.pop(board_pos)
            self.remove_widget(curr_piece)
            # Transparent "ghost" image for one turn
            self.place_ghost(board_pos, curr_colour)
        else:
            # Nothing there yet, place a stone
            filename = ["", black_filename, white_filename][colour]

            try:
                # load and place the appropriate stone image
                new_piece = Piece(self.game, source=filename)
                self.stones_by_board_pos[board_pos] = new_piece, colour
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
                self.update_moved_marker(new_piece.pos, colour)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
            #self.play_sound() TODO

    def on_touch_move(self, touch):
        if self.marker != None:
            # Move the marker position
            try:
                self.marker.pos = self.snap_to_grid(touch.pos)
            except IllegalMoveException:
                self.remove_widget(self.marker)
                self.marker = None

    def on_size(self,*args,**kwargs):
        self.set_up_grid()

    def get_gridlines(self):
        return []

class Piece(Scatter):
    source = StringProperty(None)

    def __init__(self, game, *args, **kwargs):
        game_size = game.size()
        self.scale = 9. / game_size
        super(Piece, self).__init__(*args, **kwargs)

