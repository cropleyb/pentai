from kivy.logger import Logger
from pentai.gui.screen import Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color

import pentai.base.gs_observer as gso_m
from pentai.base.pente_exceptions import *

from pentai.base.defines import *
import pentai.base.logger as log
import pentai.gui.popup as popup
from pentai.gui.scale import MyScale as my
import pentai.gui.game_gui as gg_m

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
    border_lines = ListProperty([0, 0, 0, 0])
    border_colour = ListProperty([20, 0, 0, 1])
    border_width = NumericProperty(6.0)
    #h_grid_text = StringProperty("ABCD")
    # TODO: Only the vertical offset is used so far.
    board_offset = ListProperty([0,180.0])
    confirm_rect_color = ListProperty([0, 0, 0, 0])
    confirm_text_color = ListProperty([0, 0, 0, 0])
    illegal_rect_color = ListProperty([0, 0, 0, 0])
    illegal_rect_pos = ListProperty([0, 0])
    illegal_rect_size = ListProperty([0, 0])

    def set_my_dp(self, screen_size):
        self.calc_board_offset(screen_size)

    def __init__(self, *args, **kwargs):
        self.set_global_game(None)
        super(PenteScreen, self).__init__(*args, **kwargs)

    def start_up(self, screen_size, filename):
        # GuiPlayer?
        import Queue

        self.moved_marker = [None, None, None]

        self.set_my_dp(screen_size)

        self.marker = None
        self.stones_by_board_pos = {}
        self.action_queue = Queue.Queue()
        self.moved_marker = [None, None, None]
        self.ghosts = []
        self.ghost_colour = None
        self.swap_p1_due_to_rematch = False
        self.confirmation_in_progress = None
        self.game_filename = filename

        self.turn_marker = None
        self.win_marker = Piece(13, source=win_filename)

        self.reviewing = False

    def set_global_game(self, game):
        gg_m.set_instance(game)

    def get_game(self):
        return gg_m.get_instance()

    def player_num_to_colour(self, player_num):
        return player_num

    def calc_board_offset(self, screen_size):
        x, y = screen_size
        # bo = y - x # Square board
        bo = y * .35 # Same vertical ratio
        print "Setting BO to %s" % bo
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
    def setup_turn_marker(self):
        self.turn_marker = Piece(13, source=turn_filename)

    def confirm_menu_screen(self):
        popup.ConfirmPopup.create_and_open(
                message="Go to Menu and leave this game?",
                action=self.app.show_menu_screen,
                size_hint=(.8, .2))

    def show_help(self):
        self.app.show_pente_help()

    def rematch(self):
        self.get_audio().hush_game_over_sound()
        cs = self.get_game().get_current_state()
        if cs.get_won_by():
            self.rematch_confirmed()
        else:
            popup.ConfirmPopup.create_and_open(message="Rematch and leave this game?",
                        action=self.rematch_confirmed,
                        size_hint=(.8, .2))

    def rematch_confirmed(self, *ignored):
        log.debug("Calling set_live False due to rematch")

        og = self.get_game()
        og.set_live(False, self)

        rules = og.get_rules()

        p1, p2 = self.calculate_rematch_players(og)

        g = self.gm.create_game(rules, p1, p2)
        self.app.start_game(g, self.swap_p1_due_to_rematch)

    def calculate_rematch_players(self, orig_game):
        rfp = self.config.get("PentAI", "rematch_first_player")
        og = orig_game

        # old game players
        o_p1 = og.get_player(P1)
        o_p2 = og.get_player(P2)

        if rfp == "Don't Swap":
            p1 = o_p1
            p2 = o_p2
        elif rfp == "Alternate":
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
                    # H vs. H, or C vs. C - Alternate who goes first
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
            self.swap_p1_due_to_rematch ^= True
        return p1, p2

    def create_clocks(self):
        # TODO: Ugly
        self.clocks[:] = [None]
        if self.get_game().get_total_time() > 0:
            # Time controls active.
            import gui_clock as gc_m
            for player_num, time_id in [
                    (P1, self.ids.black_time_id),
                    (P2, self.ids.white_time_id)]:
                gc = gc_m.GuiClock(player_num, time_id, self.get_game())
                self.clocks.append(gc)
        else:
            import pentai.base.mock as mock
            self.clocks.append(mock.Mock())
            self.clocks.append(mock.Mock())

    def set_game(self, game, swap_colours):
        import datetime # TODO: Remove when old file format is gone

        self.clean_board()
        self.legend_complete = False
        self.set_global_game(game)
        self.swap_p1_due_to_rematch = swap_colours
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

        self.start_game_soon()

    def is_current_screen(self):
        return self.app.is_current_screen(self)

    def start_game_soon(self, *ignored):
        while not self.is_current_screen():
            Clock.schedule_once(self.start_game_soon, 0.3)
            return
        Clock.schedule_once(self.really_start_game, 0.3)

    def really_start_game(self, *ignored):
        if self.game_filename:
            self.load_file()
        elif self.get_game().resume_move_number > 1:
            self.load_moves()
        else:
            self.make_first_move()

    def is_live(self):
        game = self.get_game()
        return game and game.is_live()

    def set_live(self, val):
        #log.debug("pente_screen set_live: %s" % val)
        was_live = self.is_live()
        game = self.get_game()
        if not game:
            if not val:
                return
            log.error("Cannot make non-existent game live")
            crash()
            return

        game.set_live(val, self)
        if val:
            if not was_live and not self.get_game().finished():
                if self.get_game().get_move_number() > 1:
                    # Transitioning to live, so get things going
                    self.prompt_for_action()

                if not self.reviewing:
                    self.start_ticking()
        else:
            self.stop_ticking()
            self.get_game().get_current_player().stop()

    # GuiPlayer?
    def make_first_move(self, *ignored):
        """
        Some rule variations require that the first black move must
        be in the center. TODO: This shouldn't really be in the GUI.
        """
        r = self.get_game().rules
        if r.center_first:
            bs = r.size
            self.get_game().make_move((bs/2, bs/2))
            self.clocks[P1].made_move()
        self.prompt_for_action()

    def display_names(self):
        from pentai.gui.fonts import AI_FONT
        for player_num in (P1, P2):
            pname = self.get_game().get_player_name(player_num)
            ptype = self.get_game().get_player_type(player_num)
            if ptype in ("Computer", "AI"):
                pname = "[font=%s]%s[/font]" % (AI_FONT, pname)
            self.player_name[player_num] = pname

        for (pn, player_id, time_id) in \
                [(1, "p1_id", "black_time_id"), \
                 (2, "p2_id", "white_time_id")]:
            c = self.get_player_colour(pn)
            self.ids[time_id].color = c
            player_widget = self.ids[player_id]
            if player_widget.color != c:
                # Workaround for color assignment not causing refresh
                player_widget.text, tmp = "", player_widget.text
                player_widget.color = c
                player_widget.text = tmp

    def get_player_colour(self, player_num):
        COL_COLS = (None, (0, 0, 0, 1), (1, 1, 1, 1))
        col_ind = self.get_player_colour_index(player_num)
        pc = COL_COLS[col_ind]
        return pc

    def get_player_colour_index(self, player_num):
        import pentai.gui.config as cf_m
        fpc = cf_m.config_instance().get("PentAI", "first_player_colour")

        ret = player_num

        if fpc == "Always White":
            ret = opposite_colour(ret)

        elif fpc == "Keep The Same":
            if self.swap_p1_due_to_rematch:
                ret = opposite_colour(ret)

        return ret

    def display_error(self, message):
        self.get_audio().beep()
        self.app.display_message(message)

    def request_move(self, name):
        # TODO: Remove need for this - compat with Text GUI
        return ""

    def enqueue_action(self, action):
        self.action_queue.put(action)
        current_player_type = self.get_game().get_current_player_type()
        mw = 0.0
        if current_player_type in ("Computer", "AI"):
            mw = self.config.getfloat("PentAI", "minimum_wait")
        Clock.schedule_once(self.trig, mw)

    def enqueue_move(self, move):
        game = self.get_game()
        turn = game.get_move_number()
        prev_move = game.get_last_move()
        action = turn, prev_move, move
        self.enqueue_action(action)

    def load_file(self, dt):
        f = open(self.game_filename)
        self.get_game().autosave_filename = self.game_filename[:]
        self.get_game().load_game(f.read())
        self.setup_grid()
        self.game_filename = None
        self.prompt_for_action()

    def load_moves(self, dt=None):
        self.get_audio().mute()
        self.get_game().resume()

        is_finished = self.get_game().get_won_by() > 0
        self.set_review_mode(is_finished)

        self.game_filename = None
        self.get_audio().unmute()
        self.prompt_for_action()

    def on_enter(self):
        if self.get_game().get_move_number() > 1:
            self.go_to_the_beginning()
            self.load_moves()

        if not self.get_game().finished():
            self.set_review_mode(False)

        import time
        time.sleep(0.5)

    def resize(self, screen_size):
        if not self.get_game():
            return
        self.set_my_dp(screen_size)

        if self.turn_marker:
            self.remove_widget(self.turn_marker)
        self.turn_marker = None

        if self.win_marker:
            self.remove_widget(self.win_marker)
        self.win_marker = None

        self.win_marker = Piece(13, source=win_filename)
        try:
            self.setup_grid()
        except:
            st()
        #st()
        self.on_enter()

    def on_pre_leave(self):
        self.leave_game()
        try:
            # Clean up moving turn marker in case it is still animated
            widget = self.get_turn_marker()
            self.anim.stop_all(widget)
        except:
            pass

    # Called from:
    # - screen mgr when we leave the screen (push or pop)
    # - demo start code (in kivy_app_main)
    # For pop / menu, we should clear out the game_gui instance.
    def leave_game(self):
        log.debug("Calling set_live False in leave_game")

        self.set_live(False)

        if not self.app.in_demo_mode():
            self.gm.save(self.get_game())
            self.get_audio().mute()
            try:
                won_by = self.get_game().get_won_by()
                if won_by:
                    add_to_ob = self.config.get("PentAI", "add_games_to_ob")
                    log.debug("Add single game to openings book: %s" % add_to_ob)
                    if add_to_ob:
                        self.ob.add_game(self.get_game(), won_by)
            except OpeningsBookDuplicateException:
                pass
            self.get_audio().unmute()

    def start_ticking(self):
        if not self.get_game().finished():
            colour = self.get_game().to_move_colour()
            self.clocks[colour].start_ticking()

    def stop_ticking(self):
        if self.get_game():
            colour = self.get_game().to_move_colour()
            self.clocks[colour].made_move() # TODO: "made_move"
            opp_colour = opposite_colour(colour)
            self.clocks[opp_colour].made_move() # TODO: "made_move"

    def perform(self, dt):
        game = self.get_game()
        move = None
        while not self.action_queue.empty():
            # Remove marker if it is currently displayed
            if self.marker:
                self.remove_widget(self.marker)

            # Remove any confirmation piece, and hide the confirmation area
            self.cancel_confirmation()
            
            action = self.action_queue.get()
            try:
                if not game.is_live():
                    log.info("Attempt was made to move while the game was not live")
                    return
            except AttributeError:
                log.info("Attempt was made to move after game was left")
                return

            if not action:
                if self.get_game().get_won_by() == (P1+P2):
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
            if not self.app.in_demo_mode():
                log.warn("No valid move found")
            return

        try:
            self.get_game().make_move(move)
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
            self.get_game().prompt_for_action(self)

    def board_size(self):
        return self.get_game().size()

    def grid_size(self):
        """ The Grid on the screen allows extra space at the edges """
        return self.get_game().size() + 1

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
        self.app.guide.on_end_of_game()

    def get_audio(self):
        import audio as a_m
        return a_m.instance

    def remove_captured_widgets(self, colour):
        cw = self.captured_widgets[colour]

        while len(cw) > 0:
            w = cw.pop()
            self.remove_widget(w)

    # KivyPlayer
    def update_captures(self, colour, captured):
        """ Update the display of captured stones below the board """
        if self.get_game().rules.stones_for_capture_win <= 0:
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
                        x = base_x + j * 7 * my.dp
                        y = base_y + i_centred * 20 * my.dp
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
        self.display_names()
        self.refresh_legend()
        self.refresh_moved_markers()
        self.refresh_captures_and_winner()
        self.refresh_ghosts()
        self.refresh_illegal()
        self.clocks[P1].refresh()
        self.clocks[P2].refresh()

    # KivyPlayer
    def get_turn_marker(self):
        if self.turn_marker is None:
            self.setup_turn_marker()
        return self.turn_marker

    def refresh_captures_and_winner(self):
        """ Update fields in the panel from changes to the game state """
        # TODO: Only call this when the game is up to date
        for colour in (P1, P2):
            level = colour
            self.update_captures(colour, self.get_game().get_captured(colour))

        if self.get_game().finished():
            widget = self.win_marker
            colour = self.get_game().get_won_by()
            other_marker = self.get_turn_marker()
            self.show_win_method()
            if self.get_game().get_won_by() == P1 + P2:
                return
        else:
            self.ids.win_method_id.text = ""
            colour = self.get_game().to_move_colour()
            widget = self.get_turn_marker()
            other_marker = self.win_marker

        if other_marker.parent != None:
            self.remove_widget(other_marker)

        size_x, size_y = self.size
        level = colour
        base_y = self.board_offset[1] * .5 * (2.5-level)
        new_pos = size_x/2, base_y

        if widget.parent == None:
            widget.pos = new_pos
            self.add_widget(widget)
        else:
            from kivy.animation import Animation
            self.anim = Animation(pos=new_pos, duration=0.2)
            self.anim.start(widget)

    def show_win_method(self):
        wm_w = self.ids.win_method_id
        wm_w.text = \
                "[b]Won by %s[/b]" % self.get_game().get_win_method()
        wm_w.font_size = 30 * my.dp

    def setup_grid_lines(self):
        size_x, size_y = self.size
        # Adjust for the position of the board being shifted so we can have a panel of
        # extra information.
        size_y -= self.board_offset[1]

        lines = []

        # This part is using the relative layout to get the lines in the right place
        # RL does not scale though.
        Color(0, 0, 0, 1) # Black lines
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

    def setup_legend(self):
        if self.legend_complete:
            # Already initialised
            return

        import string

        bs = self.board_size()

        try:
            for bl in self.legend_box_layouts:
                bl.parent.remove_widget(bl)
        except AttributeError:
            pass
        board_rgb = (0.8117, 0.4667, .2039)
        black_rgb = (0.0, 0.0, 0.0)
        self.legend_colour = \
            self.calc_contrast_colour(board_rgb, black_rgb, self.border_colour)

        self.legend_box_layouts = []

        letters = string.ascii_lowercase.replace('i','')[:bs]
        letters = "%s" % letters

        board_offset_factor_y = float(self.board_offset[1]) / self.size[1]
        tob = 0.5-board_offset_factor_y
        print "tob: %s -------------------" % tob
        print "bofy: %s size[1]: %s" % (board_offset_factor_y, self.size[1])
        '''
        : 0.35 size[1]: 396
        
        tob: 0.15 -------------------
        bofy: 0.35 size[1]: 396
        '''

        self.create_legend("horizontal", 1.0/(2*bs), 0.25/bs-0.495,
                           (float(bs)/(bs+1),None), letters)

        # top of screen is +.5, except it is shifted by the relative layout
        self.create_legend("horizontal", 1.0/(2*bs), tob-.25/bs,
                           (float(bs)/(bs+1),None), letters)

        nums = reversed(["%d" % (i+1) for i in range(bs)])
        self.create_legend("vertical", -0.476, 0.35/bs,
                           (None,0.645*(bs)/(bs+1)), nums)

        nums = reversed(["%d" % (i+1) for i in range(bs)])
        self.create_legend("vertical", 0.47, 0.35/bs,
                           (None,0.645*(bs)/(bs+1)), nums)

        self.legend_complete = True

    def create_legend(self, orientation, x_factor, y_factor, size_hint, chars):
        from kivy.uix.boxlayout import BoxLayout
        fl = self.ids.float_layout_id
        bl = BoxLayout(orientation=orientation)
        self.legend_box_layouts.append(bl)
        fl.add_widget(bl)
        self.create_legend_widgets(bl, chars)
        bl.pos_hint = {'x':x_factor, 'y':y_factor}
        if size_hint[0]:
            bl.size_hint_x = size_hint[0]
        if size_hint[1]:
            bl.size_hint_y = size_hint[1]

    def calc_contrast_colour(self, *source_colours):
        """
        Create a contrasting colour to n arbitrary RGB colours
        E.g. (a,b,c) & (d,e,f) => (g,h,i)
        All of a,b,c,d,e,f are in the range 0.0 to 1.0
        For the pair a&d, we want the number in this range that is furthest from
        the closest of these.
        """
        cc = [0,0,0,1]
        for i in (0,1,2):
            source_components = [sc[i] for sc in source_colours]
            ssc = sorted(source_components)
            candidates = [0]
            cand_vals = [ssc[0]-0.0]

            for j in range(len(ssc)-1):
                candidates.append(j)
                cand_vals.append((ssc[j+1]-ssc[j]) * 0.5)

            candidates.append(len(ssc))
            cand_vals.append(1.0-ssc[-1])

            cv_zipped = zip(cand_vals, candidates)

            cc[i] = max(cv_zipped)[1]

        return cc

    def create_legend_widgets(self, parent, chars):
        from kivy.uix.label import Label
        for i, val in enumerate(chars):
            l = Label()
            l.text = val
            l.color = self.legend_colour
            l.align = "center"
            parent.add_widget(l)

    def setup_grid(self, _dt=None):
        if self.get_game() != None:
            self.gridlines = self.setup_grid_lines()
            self.setup_legend()

    def refresh_legend(self):
        from kivy.uix.widget import WidgetException
        try:
            fl = self.ids.float_layout_id
            show = self.config.getint("PentAI", "show_legend")
            for bl in self.legend_box_layouts:
                if show:
                    fl.add_widget(bl)
                else:
                    fl.remove_widget(bl)
        except WidgetException, e:
            pass

    def snap_to_grid(self, screen_pos):
        return self.board_to_screen(self.screen_to_board(screen_pos))

    def setup_colour_border(self, size_x, size_y):
        w = 6 * my.dp
        # This is ugly, but using the "rectangle" feature causes issues in the corners
        self.border_lines = [w,w, size_x,w, w,w, w,size_y, w,size_y-w, size_x,size_y-w]
        self.border_lines.extend([size_x-w,size_y, size_x-w,w, w,w, w,0])
        # The last two points are just to fill in a point that is missing
        # at the bottom left.
        self.border_colour = self.get_game().rules.border_colour
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
        pos = board_x, board_y
        cs = self.get_game().get_current_state()
        exception = cs.is_illegal(pos)
        if exception:
            raise exception
        return pos

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
                mm = Piece(self.get_game().size()*0.5, source=filename)
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
                if self.get_game().get_move_number() > 1:
                    # TODO: Would be neater if moved_marker was cleared properly
                    if self.mark_moves():
                        if w.parent is None:
                            self.add_widget(w)

    def cancel_confirmation(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.remove_widget(widget)
            self.confirmation_in_progress = None

            # Hide confirm area and text
            self.confirm_rect_color = [0, 0, 0, 0]
            self.confirm_text_color = [0, 0, 0, 0]

    def adjust_confirmation(self, board_pos):
        if self.confirmation_in_progress:
            widget, old_board_pos = self.confirmation_in_progress
            if board_pos == old_board_pos:
                # Click on the confirm piece
                cm = self.confirm_mode()
                self.cancel_confirmation()
            else:
                # Adjust the confirmation
                widget.pos = self.board_to_screen(board_pos)
                self.confirmation_in_progress = widget, board_pos
        else:
            colour = self.get_player_colour_index(self.get_game().to_move_colour())
            cfs = confirm_filename
            filename = cfs[colour]
            widget = Piece(self.get_game().size(), source=filename)
            widget.pos = self.board_to_screen(board_pos)
            self.add_widget(widget)
            self.confirmation_in_progress = widget, board_pos
            
            # Green to confirm off board
            col = [0, 1, 0, .5]
            self.confirm_rect_color = col

            # Gray "Confirm Here"
            self.confirm_text_color = [.155, .155, .155, .50]

    def confirm_move(self):
        if self.confirmation_in_progress != None:
            widget, board_pos = self.confirmation_in_progress
            self.enqueue_move(board_pos)

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
        #st()
        players = self.get_game().get_all_players()
        human_count = 0
        for i in (1,2):
            if players[i].get_type() == "Human":
                human_count += 1
        if human_count == 0:
            self.display_error("You are not playing! (Try reviewing)")
            return

        self.reviewing = False
        self.get_audio().mute()
        self.get_game().go_backwards_one_for_gui()
        if human_count == 1:
            if self.get_game().get_current_player_type() != "Human":
                self.get_game().go_backwards_one_for_gui()
        self.get_audio().unmute()

    def go_to_the_beginning(self):
        self.get_game().go_to_the_beginning()

    def go_forwards_one(self):
        self.get_game().go_forwards_one()

    def go_backwards_one(self):
        self.get_audio().mute()
        self.get_game().go_backwards_one_for_gui()
        self.get_audio().unmute()

    def go_to_the_end(self):
        self.get_audio().mute()
        self.get_game().go_to_the_end()
        self.get_audio().unmute()

    def assess(self):
        # TODO: only in review mode
        import pentai.ai.assessor as as_m
        assessor = as_m.Assessor(self.get_game())
        log.debug("calculating best move")
        answer = assessor.calc_best_move(gui=self)
        print answer

    def on_touch_down(self, touch):
        if touch.is_double_tap or touch.is_triple_tap:
            return True

        if touch.pos[1] < self.board_offset[1]:
            # Off the playing area
            if self.confirmation_in_progress:
                if self.confirm_mode() == "Off Board":
                    self.confirm_move()
                return True

            # Let controls below the board recognize the touch
            return super(PenteScreen, self).on_touch_down(touch)
        
        # i.e. else
        if self.are_reviewing():
            return True

        # Check that it is a human's turn.
        current_player = self.get_game().get_current_player()
        if current_player.get_type() == "Human":
            # Place a marker at the (snapped) cursor position.
            if self.marker == None:
                try:
                    # load the image
                    self.marker = Piece(self.get_game().size(), \
                            source=x_filename)
                except Exception, e:
                    Logger.exception('Board: Unable to load <%s>' % x_filename)
            if self.marker.parent == self:
                # Second touch, cancel both
                self.remove_widget(self.marker)
                self.marker = None
                return True
            try:
                self.marker.pos = self.snap_to_grid(touch.pos)
                self.add_widget(self.marker)
            except OffBoardException:
                return True
            except IllegalMoveException:
                return True
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
                if self.marker.parent == None:
                    self.add_widget(self.marker)
                return

            except OffBoardException:
                if self.marker.parent != None:
                    self.remove_widget(self.marker)
                self.marker = None

            except IllegalMoveException:
                # Leave the marker at the previous position
                pass

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

                try:
                    board_pos = self.screen_to_board(self.marker.pos)
                except IllegalMoveException:
                    # Current marker position is somehow an illegal move?
                    # It should not have been possible to set it there, but we
                    # will ignore it.
                    self.remove_widget(self.marker)
                    return
                except OffBoardException:
                    # The user dragged the marker off the board (presumably below)
                    # so we will cancel that attempt to make a move.
                    self.remove_widget(self.marker)
                    return

                if self.confirm_mode():
                    self.remove_widget(self.marker)
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
            new_piece = Piece(self.get_game().size(), source=filename)
            new_piece.pos = self.board_to_screen(board_pos)
            self.ghosts.append(new_piece)
            self.add_widget(new_piece)
        except Exception, e:
            Logger.exception('Board: Unable to load <%s>' % filename)

    def refresh_illegal(self):
        game = self.get_game()
        rules = game.get_rules()
        self.illegal_rect_color = [0, 0, 0, 0]
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
                new_piece = Piece(self.get_game().size(), source=filename)
                self.stones_by_board_pos[board_pos] = new_piece, colour
                new_piece.pos = self.board_to_screen(board_pos)
                self.add_widget(new_piece)
                self.update_moved_marker(new_piece.pos, colour)
            except Exception, e:
                Logger.exception('Board: Unable to load <%s>' % filename)
            self.get_audio().place()

    def on_size(self,*args,**kwargs):
        self.legend_complete = False
        #Clock.schedule_once(lambda dt: self.resize(args[1]), 0.1)
        self.resize(args[1])
        self.setup_grid()

    def get_gridlines(self):
        return []

    def set_review_mode(self, val):
        log.debug("set_review_mode to: %s" % val)
        self.reviewing = val
        
        # TODO: Demo flag?
        log.debug("Calling set_live from set_review_mode")
        self.set_live(not val and not self.app.in_demo_mode())
        
        if val:
            cls = ReviewButtons
        else:
            cls = PlayButtons
            self.go_to_the_end()

        panel_buttons = cls()
        self.panel_buttons = panel_buttons
        panel_buttons.ps = self

        #try:
            # TODO Merge into one call
        self.app.guide.setup_pente_panel_hooks(panel_buttons)
        self.app.guide.on_pente_panel_switch(panel_buttons)
        #except AttributeError:
        #    pass

        pb_parent = self.ids.panel_buttons_id
        pb_parent.clear_widgets()
        pb_parent.add_widget(panel_buttons)

    def are_reviewing(self):
        return self.reviewing


from kivy.uix.scatter import Scatter

class Piece(Scatter):
    source = StringProperty(None)

    def __init__(self, board_size, *args, **kwargs):
        self.scale = 7.0 * my.dp / board_size
        super(Piece, self).__init__(*args, **kwargs)
        self.do_translation = False
        self.do_rotation = False
        self.do_scale = False
'''

from kivy.uix.image import Image
#from kivy.uix.widget import Widget

# TODO: Rename: ScaledImage?
# Turn marker and flag should not use this!
class Piece(Image):
    #source = StringProperty(None)
    board_size = NumericProperty(None)

    def __init__(self, board_size, source, *args, **kwargs):
        self.board_size = board_size
        self.source = source
        #super(Piece, self).__init__(*args, **kwargs)

        #Clock.schedule_once(self.redraw, .01)

        #self.my_image = Image(source=source, allow_stretch=True, center=(0,0))
        #my_image = self.my_image
        #self.bind(texture_size=self.redraw)

        #my.bind(dp=self.redraw)
        #my_image.bind(pos=self.redraw)
        #self.redraw()

        #self.add_widget(my_image)

    """
    def redraw(self, *ignored):
        print "redrawing Piece"
        #st()
        self.size = (20, 20) # * my.dp / self.board_size 
        #self.size = .1 # * my.dp / self.board_size 
        #self.size_y = self.my_image.norm_image_size[1] * my.dp / self.board_size 
        #self.pos = self.pos
    """
'''
'''
class Piece(Widget):
    source = StringProperty(None)
    board_size = NumericProperty(None)

    def __init__(self, board_size, source, *args, **kwargs):
        self.board_size = board_size
        self.source = source
        super(Piece, self).__init__(*args, **kwargs)

        self.my_image = Image(source=source, allow_stretch=True, center=(0,0))
        my_image = self.my_image
        my_image.bind(norm_image_size=self.redraw)

        my.bind(dp=self.redraw)
        my_image.bind(pos=self.redraw)
        self.redraw()

        self.add_widget(my_image)

    def redraw(self, *ignored):
        print "redrawing Piece"
        self.size_x = self.my_image.norm_image_size[0] * my.dp / self.board_size 
        #self.size_y = self.my_image.norm_image_size[1] * my.dp / self.board_size 
        self.my_image.pos = self.pos
'''

from kivy.uix.gridlayout import GridLayout

class PlayButtons(GridLayout):
    pass

class ReviewButtons(GridLayout):
    pass

