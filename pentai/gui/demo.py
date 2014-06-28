from kivy.clock import Clock

import time

#from defines import *

import random as rand_m

import pentai.base.human_player as h_m
import pentai.base.rules as r_m
import pentai.base.game as g_m
import pentai.ai.ai_genome as aig_m
import pentai.db.ai_factory as f_m
import pentai.db.players_mgr as pm_m
from pentai.base.pente_exceptions import *

import audio as a_m

def play_speech(part_num):
    a_m.instance.demo(part_num)

def sim_press(button):
    button.sim_press()
    Clock.schedule_once(button.sim_release, 0.2)

class Demo():
    def __init__(self, app, size):
        self.app = app
        self.size = size
        self.interrupted = False
        self.speed_factor = 0.65
        self.sleep_remaining = 0

        # TODO Save settings
        # for settings demo

        self.script_list = [self.rules_script1, self.rules_script2,
                self.rules_script3, self.rules_script4, self.rules_script5]
        self.script = None

    def start(self):
        a_m.instance.start_demo()
        self.play()

    def play(self, dt=None):
        if self.interrupted:
            self.script = None
            self.interrupted = False
            self.sleep_remaining = 0

        if self.sleep_remaining > 0:
            self.sleep_remaining -= 0.05
            Clock.schedule_once(self.play, 0.05)
            return

        if self.script is None:
            if len(self.script_list) == 0:
                self.finish()
                return
            self.script = self.script_list[0]()
            del self.script_list[0]

        try:
            self.sleep_remaining = self.script.next() / self.speed_factor
            self.sleep_remaining = (.8 + .4 * rand_m.random()) * self.sleep_remaining
        except (StopIteration, IllegalMoveException):
            self.script = None
            self.sleep_remaining = 0

        Clock.schedule_once(self.play, 0)


    def interrupt(self):
        self.interrupted = True

    def finish(self):
        self.app.finish_demo()

    def clean_up(self):
        Clock.unschedule(self.play)

    def rules_script1(self):
        play_speech("intersections")

        # We're already on the menu screen
        app = self.app
        ms = app.menu_screen

        yield(1)
        sim_press(ms.ids.new_game_id)
        yield(.2)

        app.show_new_game_screen()
        yield(.1)

        ss = app.setup_screen
        # TODO: Select white player type
        ss.ids.black_type_id.val = "Human"
        ss.ids.bpl_id.val = "You"
        #ss.ids.white_type_id.val = "AI"
        ss.ids.white_type_id.val = "Computer"
        # TODO: Select computer player somehow?
        ss.ids.wpl_id.val = "Killer"
        yield(2)

        sim_press(ss.ids.start_game_id)

    def mm(self, x,y):
        self.game.make_move((x,y))
        self.app.pente_screen.perform(0)
        self.app.pente_screen.refresh_all()

    def rules_script2(s):
        # Use most recent human player name
        pmgr = pm_m.PlayersMgr()
        human = pmgr.get_recent_player_names("Human", 1)[0]
        p1 = h_m.HumanPlayer(human)

        aif = f_m.AIFactory()
        genome = aig_m.AIGenome("PentAI")
        genome.use_openings_book = False
        p2 = aif.create_player(genome)

        # Create a game
        r = r_m.Rules(13, "standard")
        s.game = g_m.Game(r, p1, p2)

        # And start it...

        # demo flag: Disable prompting of players
        size = s.app.menu_screen.size
        s.app.start_game(s.game, size, demo=True)
        s.ps = s.app.pente_screen
        yield(1.2) # Compensating for .7 wait at start?!

        #play_speech("black_first")
        #yield(2)
        #yield(.3)

        play_speech("centre_first")
        yield(1.5)
        s.mm(3,4)
        yield(1)

        s.mm(6,8)
        yield(.5)
        s.mm(4,4)
        yield(.5)

        s.mm(6,7)
        yield(.5)
        s.mm(5,8)
        yield(.5)
        play_speech("line_5_wins")

        s.mm(6,9)
        yield(.5)
        s.mm(8,3)
        yield(.5)

        s.mm(6,10)
        yield(3)

        # Diagonal white win
        s.app.pente_screen.set_review_mode(False)
        s.game.go_to_the_beginning()
        yield(1)

        s.mm(6, 6)
        yield(.5)
        s.mm(5, 5)
        yield(.5)

        s.mm(4, 6)
        yield(.5)
        s.mm(7, 3)
        yield(.5)

        play_speech("diagonal_wins")

        s.mm(7, 5)
        yield(.5)
        s.mm(9, 1)
        yield(.5)

        s.mm(5, 6)
        yield(.5)
        s.mm(6, 4)
        yield(.5)

        s.mm(8, 6)
        yield(.8)
        s.mm(8, 2)
        yield(2.5)

    def rules_script3(s):
        # Captures
        s.app.pente_screen.set_review_mode(False)
        s.game.go_to_the_beginning()
        yield(1)

        s.mm(6, 6)
        yield(.5)
        s.mm(6, 7)
        yield(.5)

        play_speech("pair_captures")

        s.mm(6, 5)
        yield(1.5)
        s.mm(6, 4)
        yield(2.5)
        
        s.mm(5, 3)
        yield(.5)
        s.mm(7, 5)
        yield(1)

        play_speech("diag_capt")
        yield(1.5)

        s.mm(8, 6)
        yield(2.5)
        s.mm(6, 6)
        yield(1)

    def rules_script4(s):
        # Non captures
        ##############
        s.game.go_to_the_beginning()
        play_speech("non_capt")
        yield(2)

        # Length 1
        s.mm(0, 0)
        yield(.5)
        play_speech("single_stone")

        s.mm(0, 1)
        yield(1)
        s.mm(0, 2)
        yield(1)

        # Length 3
        s.mm(2, 1)
        yield(.5)
        s.mm(2, 0)
        yield(.5)
        play_speech("3_or_more")

        s.mm(2, 3)
        yield(.5)
        s.mm(8, 4)
        yield(.5)

        s.mm(2, 2)
        yield(1)
        s.mm(2, 4)
        yield(2)

        # Place inside the border
        s.mm(4, 1)
        yield(.5)
        s.mm(4, 0)
        yield(.5)

        play_speech("trigger_capt")

        s.mm(4, 10)
        yield(.5)
        s.mm(4, 3)
        yield(2)

        s.mm(4, 2) # Black places a piece inside, doesn't get taken
        yield(3)
        s.mm(6, 6)
        yield(1)

        # Gap
        play_speech("no_gaps")

        s.mm(6, 3)
        yield(.5)
        s.mm(6, 0)
        yield(.5)

        s.mm(6, 1)
        yield(1)
        s.mm(6, 4)
        yield(2)

        # Double capture
        s.mm(7, 6)
        yield(.5)

        play_speech("two_pairs")
        s.mm(5, 6)
        yield(.5)
        s.mm(7, 9)
        yield(.5)
        s.mm(5, 7)
        yield(.5)
        s.mm(0, 12)
        yield(.5)
        s.mm(6, 8)
        yield(.5)
        s.mm(4, 6)
        yield(2)

    def rules_script5(s):
        # 5 Pairs win the game
        s.game.go_to_the_beginning()
        play_speech("capt_win")
        yield(1)

        # 1
        s.mm(0, 1)
        yield(.3)
        s.mm(0, 0)
        yield(.3)

        s.mm(0, 2)
        yield(.3)
        s.mm(0, 3)
        yield(.3)

        # 2
        s.mm(2, 1)
        yield(.3)
        s.mm(2, 0)
        yield(.3)

        s.mm(2, 2)
        yield(.3)
        s.mm(2, 3)
        yield(.3)

        # 3
        s.mm(4, 2)
        yield(.3)
        s.mm(4, 3)
        yield(.3)

        s.mm(4, 1)
        yield(.3)
        s.mm(4, 0)
        yield(.3)

        # 4
        s.mm(7, 1)
        yield(.3)
        s.mm(6, 0)
        yield(.3)

        s.mm(8, 2)
        yield(.3)
        s.mm(9, 3)
        yield(.3)

        # 5
        s.mm(2, 10)
        yield(.3)
        s.mm(0, 12)
        yield(.3)

        s.mm(1, 11)
        yield(2)
        s.mm(3, 9)
        yield(0.5)
        play_speech("capt_no_win")
        yield(4)

        # Demonstrate review mode
        play_speech("review")

        # Click go to beginning
        beginning_button = s.ps.panel_buttons.ids.beginning_id
        sim_press(beginning_button)
        yield(.3)

        s.game.go_to_the_beginning()
        yield(.7)

        # Click forward a few times
        forward_button = s.ps.panel_buttons.ids.forward_id
        for i in range(8):
            sim_press(forward_button)
            yield(.2)

            s.game.go_forwards_one()
            yield(.5)

        yield(.2)
        play_speech("enjoy")

        yield(4)

        ########


