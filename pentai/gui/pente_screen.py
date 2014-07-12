from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.label import Label

import pentai.base.gs_observer as gso_m
from pentai.base.pente_exceptions import *

import audio as a_m
from pentai.base.defines import *
import pentai.base.logger as log
import pentai.base.mock as mock
import pentai.gui.popup as popup
import pentai.gui.config as cf_m
import gui_clock as gc_m

import Queue
import datetime # TODO: Remove when old file format is gone
import string
import time

piece_filename = (None, \
    "./media/black_transparent.png", \
    "./media/white_transparent.png")
ghost_filename = (None, \
    "./media/black_ghost.png",
    "./media/white_ghost.png")
confirm_filename = (None, \
    "./media/b_confirm.png",
    "./media/w_confirm.png")
win_filename = "./media/winning_flag.png"
turn_filename = "./media/turn_marker.png"
computer_filename = "./media/DT.png"
x_filename = "./media/X_transparent.png"
moved_marker_filename_w = "./media/moved_marker_w.png"
moved_marker_filename_b = "./media/moved_marker_b.png"

class PenteScreen(Screen, gso_m.GSObserver):
    # GuiPlayer
    player_name = ListProperty([None, "Black", "White"])
    player_time = ListProperty([None, "0:00", "0:00"])
    captured_widgets = ListProperty([None, [], []])
    clocks = ListProperty([None])

    gridlines = ListProperty([])
    border_lines = ListProperty([0,0,0,0])
    border_colour = ListProperty([20,0,0,1])
    border_width = NumericProperty(6.0)
    #h_grid_text = StringProperty("ABCD")
    # TODO: Only the vertical offset is used so far.
    board_offset = ListProperty([0,180.0])
    confirm_rect_color = ListProperty([0, 0, 0, 0])
    illegal_rect_color = ListProperty([0, 0, 0, 0])
    illegal_rect_pos = ListProperty([0, 0])
    illegal_rect_size = ListProperty([0, 0])

    def __init__(self, screen_size, filename, *args, **kwargs):
        # GuiPlayer?
        self.moved_marker = [None, None, None]

        # TODO: Use scale module
        global my_dp
        my_dp = screen_size[0] / 457.0

        self.marker = None
        self.stones_by_board_pos = {}
        self.action_queue = Queue.Queue()
        self.ghosts = []
        self.ghost_colour = None
        self.swap_colours_due_to_rematch = False
        self.confirmation_in_progress = None
        self.game = None
        self.game_filename = filename

        self.turn_markers = None
        self.win_marker = Piece(13, source=win_filename)

        self.calc_board_offset(screen_size)

        self.reviewing = False

        super(PenteScreen, self).__init__(*args, **kwargs)

    def player_num_to_colour(self, player_num):
        return player_num

    def calc_board_offset(self, screen_size):
        x, y = screen_size
        # bo = y - x # Square board
        bo = y * .35 # Same vertical ratio
        self.board_offset[1] = bo

    def clean_board(self):
        for stone, col in self.stones_by_board_pos.values():
            self.remove_widget(stone)
        self.stones_by_board_pos = {}
        self.remove_ghosts()
        self.cancel_confirmation()
        for colour in (P1, P2):
            self.remove_captured_widgets(colour)

    # GuiPlayer
    def setup_turn_markers(self):
        self.turn_markers = [None]
        for colour in [P1, P2]:
            player = self.game.get_player(colour)

            if player.get_type() == "Human":
                filename = turn_filename
            else:
                filename = computer_filename

            tm = Piece(13, source=filename)
            self.turn_markers.append(tm)

    def rematch(self):
        self.get_audio().hush_game_over_sound()
        cs = self.game.get_current_state()
        if not self.reviewing:
            self.rematch_confirmed()
        elif cs.get_won_by():
            self.rematch_confirmed()
        else:
            popup.ConfirmPopup.create_and_open(message="Rematch and leave this game?",
                        action=self.rematch_confirmed,
                        size_hint=(.8, .2),
                        force=True)

    def rematch_confirmed(self, *ignored):
        og = self.game
        og.set_live(False, self)

        rules = og.get_rules()

        p1, p2 = self.calculate_rematch_players(og)

        g = self.gm.create_game(rules, p1, p2)
        self.app.start_game(g, self.size, self.swap_colours_due_to_rematch)

    def calculate_rematch_players(self, orig_game):
        rfp = self.config.get("PentAI", "rematch_first_player")
        og = orig_game

        # old game players
        o_p1 = og.get_player(P1)
        o_p2 = og.get_player(P2)

        if rfp == "Don't swap":
            p1 = o_p1
            p2 = o_p2
        elif rfp == "Always swap":
            p1 = o_p2
            p2 = o_p1
        else:
            # "Loser first"
            o_winner = og.get_won_by()

            if o_winner != EMPTY:
                # Last game was finished - Loser goes first
                p1 = og.get_player(opposite_colour(o_winner)) # TODO: Rename to opposite_player
                p2 = og.get_player(o_winner)

            # The game was unfinished
            else:
                if o_p1.get_type() == o_p2.get_type():
                    # H vs. H, or C vs. C - Always swap who goes first
                    p1 = o_p2
                    p2 = o_p1
                else:
                    # HvC - Assume computer won, Human first
                    if o_p1.get_type() == "Human":
                        p1 = o_p1
                        p2 = o_p2
                    else:
                        p1 = o_p2
                        p2 = o_p1
        if p1 != o_p1:
            #print "Swapping colours due to rematch"
            #st()
            self.swap_colours_due_to_rematch ^= True
        return p1, p2

    def create_clocks(self):
        # TODO: Ugly
        self.clocks[:] = [None]
        if self.game.get_total_time() > 0:
            # Time controls active.
            for player_num, time_id in [
                    (P1, self.ids.black_time_id),
                    (P2, self.ids.white_time_id)]:
                gc = gc_m.GuiClock(player_num, time_id, self.game)
                self.clocks.append(gc)
        else:
            self.clocks.append(mock.Mock())
            self.clocks.append(mock.Mock())

    def set_game(self, game, swap_colours):
        self.clean_board()
        self.game = game
        self.swap_colours_due_to_rematch = swap_colours
        p1 = game.get_player_name(P1)
        p2 = game.get_player_name(P2)
        if game.autosave_filename == None:
            filename = "games/%s_%s_%s.txt" % \
                (p1,
                 p2,
                 str(datetime.date.today()))
            game.autosave_filename = filename

        # We must watch what happens to the logical board,
        # and update the screen accordingly
        cs = game.get_current_state()
        cs.add_observer(self)

        self.trig = Clock.create_trigger(self.perform)
        self.display_names()
        self.setup_grid()

        self.create_clocks()

        # This must occur before the start function
        Clock.schedule_once(lambda dt: self.set_review_mode(False), .2)

        # Need some time for kivy to finish setting up, otherwise
        # the pieces are all stacked in the bottom left corner,
        # or we get lots of GUI lag for the screen transition (AI)
        transition_time = 1.0

        start_func = self.make_first_move
        if self.game_filename:
            start_func = self.load_file
        elif not self.game.resume_move_number is None:
            start_func = self.load_moves

        Clock.schedule_once(start_func, transition_time)

    def is_live(self):
        return self.game.is_live()

    def set_live(self, val):
        log.debug("pente_screen set_live: %s" % val)
        was_live = self.is_live()
        self.game.set_live(val, self)
        if val:
            if not was_live and not self.game.finished():
                if self.game.get_move_number() > 1:
                    # Transitioning to live, so get things going
                    #print "set_live prompt_for_action"
                    self.prompt_for_action()

                if not self.reviewing:
                    self.start_ticking()
        else:
            self.stop_ticking()
            self.game.get_current_player().stop()

    # GuiPlayer?
    def make_first_move(self, dt):
        """
        Some rule variations require that the first black move must
        be in the center. TODO: This shouldn't really be in the GUI.
        """
        r = self.game.rules
        if r.center_first:
            bs = r.size
            self.game.make_move((bs/2, bs/2))
            self.refresh_all()
            self.clocks[P1].made_move()
        #print "make_first_move prompt_for_action"
        self.prompt_for_action()

    # GuiPlayer
    def display_names(self):
        for player_num in (P1, P2):
            self.player_name[player_num] = self.game.get_player_name(player_num)

        c1 = self.get_player_colour(1)
        self.ids.p1_id.color = c1
        self.ids.black_time_id.color = c1

        c2 = self.get_player_colour(2)
        self.ids.p2_id.color = c2
        self.ids.white_time_id.color = c2

    def get_player_colour(self, player_num):
        COL_COLS = (None, (0,0,0,1), (1,1,1,1))
        pc = COL_COLS[self.get_player_colour_index(player_num)]
        return pc

    def get_player_colour_index(self, player_num):
        fpc = cf_m.config_instance().get("PentAI", "first_player_colour")

        ret = player_num

        if fpc == "Always White":
            ret = opposite_colour(ret)

        elif fpc == "Keep the same":
            if self.swap_colours_due_to_rematch:
                ret = opposite_colour(ret)

        return ret

    def display_error(self, message):
        #st()
        self.get_audio().beep()
        self.app.display_error(message)

    def request_move(self, name):
        # TODO: Remove need for this - compat with Text GUI
        return ""

    def enqueue_action(self, action):
        self.action_queue.put(action)
        mw = self.config.getfloat("PentAI", "minimum_wait")
        Clock.schedule_once(self.trig, mw)

    def enqueue_move(self, move):
        game = self.game
        turn = game.get_move_number()
        prev_move = game.get_last_move()
        action = turn, prev_move, move
        self.enqueue_action(action)

    def load_file(self, dt):
        f = open(self.game_filename)
        self.game.autosave_filename = self.game_filename[:]
        self.game.load_game(f.read())
        self.setup_grid()
        self.game_filename = None
        self.refresh_all()
        #print "load_file prompt_for_action"
        self.prompt_for_action()

    def load_moves(self, dt=None):
        self.get_audio().mute()
        self.game.resume()
        self.game_filename = None
        self.refresh_all()
        self.get_audio().unmute()
        #print "load_moves prompt_for_action"
        self.prompt_for_action()

    def on_enter(self):
        if self.game.get_move_number() > 1:
            self.go_to_the_beginning()
            self.load_moves()

        self.refresh_all()
        if not self.game.finished():
            self.set_review_mode(False)
        time.sleep(0.5)

    def on_pre_leave(self):
        self.set_live(False)
        if not self.app.in_demo_mode():
            self.gm.save(self.game)
            self.get_audio().mute()
            try:
                won_by = self.game.get_won_by()
                if won_by:
                    add_to_ob = self.config.get("PentAI", "add_games_to_ob")
                    log.debug("Add games to openings book: %s" % add_to_ob)
                    if add_to_ob:
                        self.ob.add_game(self.game, won_by)
            except OpeningsBookDuplicateException:
                pass
            self.get_audio().unmute()

    def start_ticking(self):
        if not self.game.finished():
            colour = self.game.to_move_colour()
            self.clocks[colour].start_ticking()

    def stop_ticking(self):
        if self.game:
            colour = self.game.to_move_colour()
            self.clocks[colour].made_move() # TODO: "made_move"
            opp_colour = opposite_colour(colour)
            self.clocks[opp_colour].made_move() # TODO: "made_move"

    def perform(self, dt):
        game = self.game
        move = None
        while not self.action_queue.empty():
            action = self.action_queue.get()
            if not game.is_live():
                return
            if not action:
                if self.game.get_won_by() == (P1+P2):
                    log.info("Draw detected")
                    # TODO: return? GUI feedback?
                return
            turn, prev_move, move = action
            if turn != game.get_move_number():
                log.warn("Turn number %s != expected %s" % (turn, game.get_move_number()))
                move = None
                continue
            if prev_move != game.get_last_move():
                log.warn("prev_move %s != expected %s" % (prev_move, game.get_last_move()))
                move = None
                continue

        if not move:
            return

        try:
            self.game.make_move(move)
            self.refresh_all()
            self.prompt_for_action()
        except Exception, e:
            self.display_error(e.message)

    def prompt_for_action(self, *ignored):
        Clock.schedule_once(self.prompt_for_action_inner, 0.01)

    def prompt_for_action_inner(self, *ignored):
        if self.is_live() and not self.reviewing:
            # TODO: game.prompt_for_action if not finished?
            self.start_ticking()
            self.game.prompt_for_action(self)

    def board_size(self):
        return self.game.size()

    def grid_size(self):
        """ The Grid on the screen allows extra space at the edges """
        return self.game.size() + 1

    def reset_state(self, game):
        """ Callback from game_state """
        self.clean_board()

    def after_set_occ(self, game, pos, colour):
        self.make_move_on_the_gui_board(pos, colour)

        if colour:
            self.clocks[colour].made_move() # TODO: "made_move"

    def up_to_date(self, game):
        self.refresh_all()

    def after_game_won(self, game, colour):
        # Play win or loss sound
        if game.get_player(colour).get_type() == "Human":
            self.get_audio().win()
        else:
            self.get_audio().lose()

        # TODO: draw, and AI vs. AI sounds
        self.refresh_all()

        self.set_review_mode(True)

    def get_audio(self):
        return a_m.instance

    def remove_captured_widgets(self, colour):
        cw = self.captured_widgets[colour]

        while len(cw) > 0:
            w = cw.pop()
            self.remove_widget(w)

    # KivyPlayer
    def update_captures(self, colour, captured):
        """ Update the display of captured stones below the board """
        if self.game.rules.stones_for_capture_win <= 0:
            # Don't display them if the rules prevent capture wins
            return
        cw = self.captured_widgets[colour]

        if len(cw) != captured:
            # It has changed. Remove them all first
            self.remove_captured_widgets(colour)

            # We capture pieces of the opposite colour
            filename = piece_filename[
                    self.get_player_colour_index(opposite_colour(colour))]
            size_x, size_y = self.size
            base_x = .95 * size_x

            level = colour

            base_y = self.board_offset[1] * .5 * (2.2-level)
            # Could capture more than one pair for the win, prevent crash
            centre = [2, 1, 3, 0, 4, -1, 5]

            for i in range(captured / 2):
                try:
                    i_centred = centre[i]
                except IndexError:
                    i_centred = 0
                for j in range(2): # TODO Use triples for keryo
                    try:
                        # load and place the appropriate stone image
                        new_piece = Piece(19, source=filename)
                        x = base_x + j * 7 * self.get_my_dp()
                        y = base_y + i_centred * 20 * self.get_my_dp()
                        new_piece.pos = x,y
                        cw.append(new_piece)
                        self.add_widget(new_piece)
                    except Exception, e:
                        log.error(e)
            if captured > 0:
                audio = self.get_audio()
                if not audio.muted:
                    Clock.schedule_once(audio.capture , 0.2)

    def refresh_all(self):
        # KivyPlayer
        self.display_names()
        self.refresh_moved_markers()
        self.refresh_captures_and_winner()
        self.refresh_ghosts()
        self.refresh_illegal()
        self.clocks[P1].refresh()
        self.clocks[P2].refresh()

    # KivyPlayer
    def get_turn_marker(self, colour):
        if self.turn_markers is None:
            self.setup_turn_markers()
        return self.turn_markers[colour]

    # KivyPlayer
    def refresh_captures_and_winner(self):
        """ Update fields in the panel from changes to the game state """
        # TODO: Only call this when the game is up to date
        for colour in (P1, P2):
            level = colour
            self.update_captures(colour, self.game.get_captured(colour))

        # TODO: Show draws somehow
        if self.game.get_won_by() == P1 + P2:
            log.warn("TODO! Display draws as such!")
            return

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

        base_y = self.board_offset[1] * .5 * (2.5-level)

        widget.pos = size_x/2, base_y

    def get_my_dp(self):
        return my_dp

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

    def setup_grid_text(self):
        hg = self.ids.lower_horiz_grid_id
        if len(hg.children) > 0:
            return
        hg.pos = self.board_to_screen((0,0))

        hgg = hg.children[0]
        l = Label()
        l.text = "Help!"
        hgg.add_widget(l)

        '''
        chars = string.ascii_uppercase.replace('I','')[:self.board_size()]
        chars = "%s " % chars
        for val in chars:
            l = Label()
            l.text = val
            l.color = 0, 0, 0, 1
            hgg.add_widget(l)
        '''

    def setup_grid(self, _dt=None):
        if self.game != None:
            self.gridlines = self.setup_grid_lines()
            #self.h_grid_text = "ABC"
            self.setup_grid_text()

    def snap_to_grid(self, screen_pos):
        return self.board_to_screen(self.screen_to_board(screen_pos))

    def setup_colour_border(self, size_x, size_y):
        w = 6 * my_dp
        # This is ugly, but using the "rectangle" feature causes issues in the corners
        self.border_lines = [w,w, size_x,w, w,w, w,size_y, w,size_y-w, size_x,size_y-w]
        self.border_lines.extend([size_x-w,size_y, size_x-w,w, w,w, w,0])
        # The last two points are just to fill in a point that is missing
        # at the bottom left.
        self.border_colour = self.game.rules.border_colour
        self.border_width = w

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
            if colour == P1:
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
                if self.mark_moves() == 1:
                    if w.parent is None:
                        self.add_widget(w)

    def cancel_confirmation(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.remove_widget(widget)
            self.confirmation_in_progress = None
            self.confirm_rect_color = [0, 0, 0, 0]

    def adjust_confirmation(self, board_pos):
        if self.confirmation_in_progress:
            widget, old_board_pos = self.confirmation_in_progress
            if board_pos == old_board_pos:
                # Click on the confirm piece
                cm = self.confirm_mode()
                if cm == "Off Board":
                    self.cancel_confirmation()
                elif cm == "On Piece":
                    self.confirm_move()
            else:
                # Adjust the confirmation
                widget.pos = self.board_to_screen(board_pos)
                self.confirmation_in_progress = widget, board_pos
        else:
            colour = self.get_player_colour_index(self.game.to_move_colour())
            #cfs = [None, black_confirm_filename, white_confirm_filename]
            cfs = confirm_filename
            filename = cfs[colour]
            widget = Piece(self.game.size(), source=filename)
            widget.pos = self.board_to_screen(board_pos)
            self.add_widget(widget)
            self.confirmation_in_progress = widget, board_pos
            if self.confirm_mode() == "Off Board":
                # Green to confirm off board
                col = [0, 1, 0, .5]
            elif self.confirm_mode() == "On Piece":
                # Red to confirm off board
                col = [1, 0, 0, .5]

            self.confirm_rect_color = col

    def confirm_move(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.enqueue_move(board_pos)
            self.cancel_confirmation()

    def confirm_mode(self):
        cm = self.config.get("PentAI", "move_confirmation")
        if cm == "None Required":
            cm = None
        return cm

    def mark_moves(self):
        return self.config.getint("PentAI", "mark_moves")

    def show_ghosts(self):
        return self.config.getint("PentAI", "mark_captures")

    def take_back_move(self):
        players = self.game.get_all_players()
        if players[1].get_type() != "Human" and \
            players[2].get_type() != "Human":
            self.display_error("You are not playing! (Try reviewing)")
            return
        self.reviewing = False
        self.get_audio().mute()
        self.game.go_backwards_one()
        self.get_audio().unmute()

    def go_to_the_beginning(self):
        self.game.go_to_the_beginning()

    def go_forwards_one(self):
        self.game.go_forwards_one()

    def go_backwards_one(self):
        self.get_audio().mute()
        self.game.go_backwards_one()
        self.get_audio().unmute()

    def go_to_the_end(self):
        self.get_audio().mute()
        self.game.go_to_the_end()
        self.get_audio().unmute()

    def on_touch_down(self, touch):
        if touch.is_double_tap or touch.is_triple_tap:
            return True

        if touch.pos[1] < self.board_offset[1]:
            if self.confirmation_in_progress:
                if self.confirm_mode() == "Off Board":
                    self.confirm_move()
                elif self.confirm_mode() == "On Piece":
                    self.cancel_confirmation()
                return True

            # Controls below the board recognized the touch
            return super(PenteScreen, self).on_touch_down(touch)
        
        # i.e. else
        if self.are_reviewing():
            return True

        # Check that it is a human's turn.
        current_player = self.game.get_current_player()
        if current_player.get_type() == "Human":
            # Place a marker at the (snapped) cursor position.
            if self.marker == None:
                try:
                    # load the image
                    self.marker = Piece(self.game.size(), \
                            source=x_filename)
                except Exception, e:
                    Logger.exception('Board: Unable to load <%s>' % x_filename)
            if self.marker.parent == self:
                # Second touch, cancel both?
                self.remove_widget(self.marker)
                self.marker = None
                return True
            try:
                self.marker.pos = self.snap_to_grid(touch.pos)
            except OffBoardException:
                return True
            self.add_widget(self.marker)
        else:
            self.display_error("It is not your turn!")

    def on_touch_move(self, touch):
        if touch.pos[1] < self.board_offset[1]:
            # This is assuming that controls below the board
            # are only using touch down.
            return True
        if self.are_reviewing():
            return True
        if self.marker != None:
            # Move the marker position
            try:
                self.marker.pos = self.snap_to_grid(touch.pos)
            except OffBoardException:
                self.remove_widget(self.marker)
                self.marker = None

    def on_touch_up(self, touch):
        # This is assuming that controls below the board
        # are only using touch down.

        if touch.pos[1] > self.board_offset[1]:
            if self.are_reviewing():
                return True
            
            # Upper section of the screen
            # If there is an active marker,
            # replace the marker with a piece of the appropriate colour
            if self.marker != None:
                self.remove_widget(self.marker)

                try:
                    board_pos = self.screen_to_board(touch.pos)
                except OffBoardException:
                    return

                if self.confirm_mode():
                    self.adjust_confirmation(board_pos)
                else:
                    # Queue the move, this will place the
                    # new piece widget appropriately
                    self.enqueue_move(board_pos)

    def refresh_ghosts(self):
        for g in self.ghosts:
            if self.show_ghosts():
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
        #filename = ["", black_ghost_filename, white_ghost_filename][colour]
        filename = ghost_filename[self.get_player_colour_index(colour)]

        try:
            # load and place the appropriate stone image
            new_piece = Piece(self.game.size(), source=filename)
            new_piece.pos = self.board_to_screen(board_pos)
            self.ghosts.append(new_piece)
            self.add_widget(new_piece)
        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % filename)

    def refresh_illegal(self):
        game = self.game
        rules = game.get_rules()
        self.illegal_rect_color = [0,0,0,0]
        if (game.get_move_number() == 3) and (rules.type_char == 't'):
            self.illegal_rect_color = [1, 0, 0, .5]
            left = game.size()/2 - 2.5

            irp = list(self.board_to_screen((left, left)))
            irp[1] -= self.board_offset[1]
            self.illegal_rect_pos = irp

            size_x, size_y = self.size
            size_y -= self.board_offset[1]

            # Use float() to avoid python int / int = int prob
            gs = float(self.grid_size())
            width = 5
            screen_x = (width / gs) * size_x
            screen_y = (width / gs) * size_y
            self.illegal_rect_size = (screen_x, screen_y)

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
            #filename = ["", black_filename, white_filename][colour]
            filename = piece_filename[self.get_player_colour_index(colour)]

            try:
                # load and place the appropriate stone image
                new_piece = Piece(self.game.size(), source=filename)
                self.stones_by_board_pos[board_pos] = new_piece, colour
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
                self.update_moved_marker(new_piece.pos, colour)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
            self.get_audio().place()

    def on_size(self,*args,**kwargs):
        self.setup_grid()

    def get_gridlines(self):
        return []

    def set_review_mode(self, val):
        log.debug("set_review_mode to: %s" % val)
        self.reviewing = val
        
        # TODO: Demo flag?
        self.set_live(not val and not self.app.in_demo_mode())
        
        if val:
            cls = ReviewButtons
        else:
            cls = PlayButtons
            self.go_to_the_end()

        panel_buttons = cls()
        self.panel_buttons = panel_buttons
        panel_buttons.ps = self
        pb_parent = self.ids.panel_buttons_id
        pb_parent.clear_widgets()
        pb_parent.add_widget(panel_buttons)

    def are_reviewing(self):
        return self.reviewing


class Piece(Scatter):
    source = StringProperty(None)

    def __init__(self, board_size, *args, **kwargs):
        self.scale = my_dp * 7.0 / board_size
        super(Piece, self).__init__(*args, **kwargs)
        self.do_translation = False
        self.do_rotation = False
        self.do_scale = False

from kivy.uix.gridlayout import GridLayout

class PlayButtons(GridLayout):
    pass

class ReviewButtons(GridLayout):
    pass

