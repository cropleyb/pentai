from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import *
#from kivy.core.audio import SoundLoader # TODO
from evaluator import *
from utility_calculator import *

from defines import *
from gui import *

import Queue
import datetime

import pdb

black_filename = "./media/black_transparent.png"
white_filename = "./media/white_transparent.png"
black_ghost_filename = "./media/black_ghost.png"
white_ghost_filename = "./media/white_ghost.png"
black_confirm_filename = "./media/b_confirm.png"
white_confirm_filename = "./media/w_confirm.png"
win_filename = "./media/winning_flag.png"
turn_filename = "./media/turn_marker.png"
computer_filename = "./media/DT.png"
x_filename = "./media/X_transparent.png"
moved_marker_filename_w = "./media/moved_marker_w.png"
moved_marker_filename_b = "./media/moved_marker_b.png"
stone_sound = "./media/click.mp3"

class PenteScreen(Screen):
    source = StringProperty(None)
    # TODO: Get the times hooked up
    player_name = ListProperty([None, "Black", "White"])
    player_time = ListProperty([None, "0:00", "0:00"])
    captured_widgets = ListProperty([None, [], []])
    gridlines = ListProperty([])
    border_lines = ListProperty([0,0,0,0])
    border_colour = ListProperty([20,0,0,1])
    # TODO: Only the vertical offset is used so far.
    board_offset = ListProperty([0,180.0])

    def __init__(self, the_size, filename, *args, **kwargs):
        self.marker = None
        self.stones_by_board_pos = {}
        self.action_queue = Queue.Queue()
        self.moved_marker = [None, None, None]
        self.mark_moves = True
        self.ghosts = []
        self.ghost_colour = None
        self.show_ghosts = True
        self.confirm_mode = None
        self.confirmation_in_progress = None
        self.game = None
        self.game_filename = filename

        self.turn_markers = None
        self.win_marker = Piece(13, source=win_filename)

        self.calc_board_offset(the_size)

        super(PenteScreen, self).__init__(*args, **kwargs)

    def calc_board_offset(self, the_size):
        x, y = the_size
        # bo = y - x # Square board
        bo = y * .35 # Same vertical ratio
        self.board_offset[1] = bo

    def clean_board(self):
        for stone, col in self.stones_by_board_pos.values():
            self.remove_widget(stone)
        self.stones_by_board_pos = {}
        self.remove_ghosts()
        self.cancel_confirmation()

    def reset_state(self):
        """ Callback from game_state """
        self.clean_board()

    def setup_turn_markers(self):
        self.turn_markers = [None]
        for colour in [BLACK, WHITE]:
            player = self.game.get_player(colour)

            if player.get_type() == "human":
                filename = turn_filename
            else:
                filename = computer_filename

            tm = Piece(13, source=filename)
            self.turn_markers.append(tm)

    def set_game(self, game):
        self.clean_board()
        self.game = game
        if game.autosave_filename == None:
            filename = "games/%s_%s_%s.txt" % \
                (game.get_player_name(BLACK),
                 game.get_player_name(WHITE),
                 str(datetime.date.today()))
            game.autosave_filename = filename

        # We must watch what happens to the logical board, and update accordingly
        cs = game.get_current_state()
        cs.add_observer(self)

        self.evaluator = Evaluator(UtilityCalculator(), cs)

        self.trig = Clock.create_trigger(self.perform)
        self.display_names()
        self.setup_grid()

        # Need some time for kivy to finish setting up, otherwise
        # the pieces are all stacked in the bottom left corner,
        # or we get lots of GUI lag for the screen transition (AI)
        transition_time = 0.7

        start_func = self.make_first_move
        if len(self.game_filename) > 0:
            start_func = self.load_file

        Clock.schedule_once(start_func, transition_time)

    def make_first_move(self, dt):
        """
        Some rule variations require that the first black move must
        be in the center. TODO: This shouldn't really be in the GUI.
        """
        r = self.game.rules
        if r.center_first:
            bs = r.size
            self.game.make_move((bs/2, bs/2))
        self.game.prompt_for_action(self)

    def display_names(self):
        flip = self.calc_flip()
        for colour in (BLACK, WHITE):
            level = colour
            if flip:
                level = opposite_colour(level)
            self.player_name[level] = self.game.get_player_name(colour)

    def display_error(self, message):
        self.app.display_error(message)

    def request_move(self, name):
        # TODO: Remove need for this - compat with Text GUI
        return ""

    def enqueue_action(self, action):
        self.action_queue.put(action)
        self.trig()

    def load_file(self, dt):
        f = open(self.game_filename)
        self.game.autosave_filename = self.game_filename[:]
        self.game.load_game(f.read())
        self.setup_grid()
        self.game_filename = None
        self.refresh_all()
        self.game.prompt_for_action(self)

    def on_enter(self):
        self.refresh_all()

    def perform(self, dt):
        if self.action_queue.empty():
            return
        action = self.action_queue.get()
        try:
            self.game.make_move(action)
            self.refresh_all()
            Clock.schedule_once(self.prompt_for_action, 0)
        except Exception, e:
            if self.game.was_interrupted():
                return
            self.display_error(e.message)

    def prompt_for_action(self, ignored):
        self.game.prompt_for_action(self)
        print self.evaluator.utility()

    def board_size(self):
        return self.game.size()

    def grid_size(self):
        """ The Grid on the screen allows extra space at the edges """
        return self.game.size() + 1

    def before_set_occ(self, pos, colour):
        pass

    def after_set_occ(self, pos, colour):
        self.make_move_on_the_gui_board(pos, colour)
        self.refresh_all()

    def after_game_won(self, game, colour):
        # TODO: play win or loss sound
        pass

    def play_sound(self):
        self.sound = SoundLoader.load(stone_sound)
        if self.sound:
            print("Sound found at %s" % self.sound.source)
            print("Sound is %.3f seconds" % self.sound.length)
        self.sound.play()

    def update_captures(self, colour, captured, flip):
        """ Update the display of captured stones below the board """
        if self.game.rules.stones_for_capture_win <= 0:
            # Don't display them if the rules prevent capture wins
            return
        cw = self.captured_widgets[colour]

        if len(cw) != captured:
            # It has changed. Remove them all first
            while len(cw) > 0:
                w = cw.pop()
                self.remove_widget(w)
            # We capture pieces of the opposite colour
            filename = ["", black_filename, white_filename] \
                    [opposite_colour(colour)]
            size_x, size_y = self.size
            base_x = .9 * size_x

            level = colour
            if flip:
                level = opposite_colour(level)

            base_y = self.board_offset[1] * .5 * (2.2-level)
            centre = [2, 1, 3, 0, 4]

            for i in range(captured / 2):
                i_centred = centre[i]
                for j in range(2): # TODO Use triples for keryo
                    try:
                        # load and place the appropriate stone image
                        new_piece = Piece(19, source=filename)
                        x = base_x + j * 7
                        y = base_y + i_centred * 20
                        new_piece.pos = x,y
                        cw.append(new_piece)
                        self.add_widget(new_piece)
                    except Exception, e:
                        print e

    def refresh_all(self):
        self.display_names()
        self.refresh_moved_markers()
        self.refresh_captures_and_winner()
        self.refresh_ghosts()

    def get_turn_marker(self, colour):
        if self.turn_markers is None:
            self.setup_turn_markers()
        return self.turn_markers[colour]

    def calc_flip(self):
        white_player = self.game.get_player(WHITE)
        black_player = self.game.get_player(BLACK)

        if white_player.get_type() == "human" and \
           black_player.get_type() != "human":
            return True
        return False

    def refresh_captures_and_winner(self):
        """ Update fields in the panel from changes to the game state """
        # TODO: Only call this when the game is up to date
        flip = self.calc_flip()
        for colour in (BLACK, WHITE):
            level = colour
            if flip:
                level = opposite_colour(level)
            self.update_captures(colour, self.game.get_captured(colour), flip)

        if self.game.finished():
            widget = self.win_marker
            colour = self.game.get_won_by()
            other_markers = [self.get_turn_marker(colour)]
        else:
            colour = self.game.to_move_colour()
            widget = self.get_turn_marker(colour)
            other_markers = [self.win_marker]

        other_markers.append(self.get_turn_marker(opposite_colour(colour)))
        if widget.parent == None:
            self.add_widget(widget)
        for om in other_markers:
            if om.parent != None:
                self.remove_widget(om)

        size_x, size_y = self.size

        level = colour
        if flip:
            level = opposite_colour(level)

        base_y = self.board_offset[1] * .5 * (2.5-level)

        widget.pos = size_x/2, base_y

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
        w = 6 # TODO this is copied and pasted from kv
        # This is ugly, but using the "rectangle" feature causes issues in the corners
        self.border_lines = [w,w, size_x,w, w,w, w,size_y, w,size_y-w, size_x,size_y-w]
        self.border_lines.extend([size_x-w,size_y, size_x-w,w, w,w, w,0])
        # The last two points are just to fill in a point that is missing
        # at the bottom left.
        self.border_colour = self.game.rules.border_colour

    def setup_grid(self, _dt=None):
        if self.game != None:
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
            raise OffBoardException
        return board_x, board_y

    def board_to_screen(self, board_pos):
        """ Convert a board coordinate pair to a screen position (in pixels),
            dependant on the size of the board """
        size_x, size_y = self.size
        size_y -= self.board_offset[1]

        # Use float() to avoid python int / int = int prob
        gs = float(self.grid_size())
        screen_x = ((board_pos[0] + 1) / gs) * size_x
        screen_y = ((board_pos[1] + 1) / gs) * size_y
        screen_y += self.board_offset[1]
        return screen_x, screen_y

    def update_moved_marker(self, pos, colour):
        mm = self.moved_marker[colour]
        if mm == None:
            filename = moved_marker_filename_w
            if colour == BLACK:
                filename = moved_marker_filename_b
            try:
                mm = Piece(self.game.size(), source=filename)
                self.moved_marker[colour] = mm
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
                return
        mm.pos = pos

    def refresh_moved_markers(self):
        for w in self.moved_marker:
            if not w is None:
                # Remove them both first
                if not w.parent is None:
                    self.remove_widget(w)
                # Then put them back ON TOP OF THE PIECES
                if self.mark_moves:
                    if w.parent is None:
                        self.add_widget(w)

    def cancel_confirmation(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.remove_widget(widget)
            self.confirmation_in_progress = None

    def adjust_confirmation(self, board_pos):
        if self.confirmation_in_progress:
            widget, old_board_pos = self.confirmation_in_progress
            if board_pos == old_board_pos:
                # Click on the confirm piece
                if self.confirm_mode == "Off Board":
                    self.cancel_confirmation()
                elif self.confirm_mode == "On Piece":
                    self.confirm_move()
            else:
                # Adjust the confirmation
                widget.pos = self.board_to_screen(board_pos)
                self.confirmation_in_progress = widget, board_pos
        else:
            colour = self.game.to_move_colour()
            cfs = [None, black_confirm_filename, white_confirm_filename]
            filename = cfs[colour]
            widget = Piece(self.game.size(), source=filename)
            widget.pos = self.board_to_screen(board_pos)
            self.add_widget(widget)
            self.confirmation_in_progress = widget, board_pos

    def confirm_move(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.enqueue_action(board_pos)
            self.cancel_confirmation()

    def set_confirm_mode(self, req):
        self.confirm_mode = req
        self.cancel_confirmation()

    def set_mark_moves(self, mm):
        self.mark_moves = mm

    def set_mark_captures(self, mc):
        self.show_ghosts = mc

    def go_to_the_beginning(self):
        self.game.go_to_the_beginning()
        self.refresh_all()
        print self.evaluator.utility()

    def go_forwards_one(self):
        self.game.go_forwards_one()
        self.refresh_all()
        print self.evaluator.utility()

    def go_backwards_one(self):
        self.game.go_backwards_one()
        self.refresh_all()
        print self.evaluator.utility()

    def go_to_the_end(self):
        self.game.go_to_the_end()
        self.refresh_all()
        print self.evaluator.utility()

    def on_touch_down(self, touch):
        if touch.pos[1] < self.board_offset[1]:
            # Controls below the board recognized the touch
            super(PenteScreen, self).on_touch_down(touch)

            # Assuming all controls are to the left of this
            if touch.pos[0] > self.size[0] * .25:
                # No controls clicked below the board-> confirm or cancel
                if self.confirm_mode == "Off Board":
                    self.confirm_move()
                elif self.confirm_mode == "On Piece":
                    self.cancel_confirmation()
            return True

        # Check that it is a human's turn.
        current_player = self.game.get_current_player()
        if current_player.get_type() == "human":
            # Place a marker at the (snapped) cursor position.
            if self.marker == None:
                try:
                    # load the image
                    self.marker = Piece(self.game.size(), \
                            source=x_filename)
                except Exception, e:
                    Logger.exception('Board: Unable to load <%s>' % x_filename)
            self.marker.pos = self.snap_to_grid(touch.pos)
            self.add_widget(self.marker)
        else:
            self.display_error("It is not your turn!")

    def on_touch_up(self, touch):
        # This is assuming that controls below the board
        # are only using touch down.

        if touch.pos[1] > self.board_offset[1]:
            # Upper section of the screen
            # If there is an active marker,
            # replace the marker with a piece of the appropriate colour
            if self.marker != None:
                self.remove_widget(self.marker)

                try:
                    board_pos = self.screen_to_board(touch.pos)
                except OffBoardException:
                    return

                if self.confirm_mode:
                    self.adjust_confirmation(board_pos)
                else:
                    # Queue the move, this will place the
                    # new piece widget appropriately
                    self.enqueue_action(board_pos)

    def refresh_ghosts(self):
        for g in self.ghosts:
            if self.show_ghosts:
                if g.parent is None:
                    self.add_widget(g)
            elif not g.parent is None:
                self.remove_widget(g)

    def remove_ghosts(self):
        while len(self.ghosts) > 0:
            g = self.ghosts.pop()
            if not g.parent is None:
                self.remove_widget(g)

    def place_ghost(self, board_pos, colour):
        if colour != self.ghost_colour:
            self.remove_ghosts()
        self.ghost_colour = colour
        filename = ["", black_ghost_filename, white_ghost_filename][colour]

        try:
            # load and place the appropriate stone image
            new_piece = Piece(self.game.size(), source=filename)
            new_piece.pos = self.board_to_screen(board_pos)
            self.ghosts.append(new_piece)
            self.add_widget(new_piece)
        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % filename)

    def make_move_on_the_gui_board(self, board_pos, colour):
        if colour == self.ghost_colour:
            self.remove_ghosts()
        if self.stones_by_board_pos.has_key(board_pos) or colour == EMPTY:
            # TODO: It would be cleaner if this was handled by a separate
            # removed stone notification. (or two: capture, undo)
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
                new_piece = Piece(self.game.size(), source=filename)
                self.stones_by_board_pos[board_pos] = new_piece, colour
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
                self.update_moved_marker(new_piece.pos, colour)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
            #self.play_sound() TODO

    def on_touch_move(self, touch):
        if touch.pos[1] < self.board_offset[1]:
            # This is assuming that controls below the board
            # are only using touch down.
            return True
        if self.marker != None:
            # Move the marker position
            try:
                self.marker.pos = self.snap_to_grid(touch.pos)
            except OffBoardException:
                self.remove_widget(self.marker)
                self.marker = None

    def on_size(self,*args,**kwargs):
        self.setup_grid()

    def get_gridlines(self):
        return []

'''
class Image(Scatter):
    source = StringProperty(None)

    def __init__(self, *args, **kwargs):
        #self.scale = 7. / board_size
        super(Piece, self).__init__(*args, **kwargs)
'''


class Piece(Scatter):
    source = StringProperty(None)

    def __init__(self, board_size, *args, **kwargs):
        self.scale = 7. / board_size
        super(Piece, self).__init__(*args, **kwargs)

