from kivy.clock import Clock

import time

from defines import *

import random as rand_m

import ai_genome as aig_m
import ai_factory as f_m
import human_player as h_m
import players_mgr as pm_m
import rules as r_m
import game as g_m
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
        #self.speed_factor = 1.5

        # TODO Save settings
        # for settings demo

        # TODO Intercept Input

        self.script = self.rules_script()

    def start(self):
        a_m.instance.start_demo()
        self.play()

    def play(self, dt=None):
        try:
            sleep_time = self.script.next() / self.speed_factor

        except StopIteration:
            self.finish()
            return

        if self.interrupted:
            self.finish()
            return

        if sleep_time != None:
            sleep_time = (.8 + .4 * rand_m.random()) * sleep_time
            Clock.schedule_once(self.play, sleep_time)

    def interrupt(self):
        self.interrupted = True

    def finish(self):
        a_m.instance.finish_demo()
        self.app.finish_demo()


    def rules_script(self):
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
        ss.ids.white_type_id.val = "Computer"
        # TODO: Select computer player somehow?
        ss.ids.wpl_id.val = "PentAI"

        yield(1)

        yield(1)
        sim_press(ss.ids.start_game_id)

        yield(.2)

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
        game = g_m.Game(r, p1, p2)

        # And start it...

        # demo flag: Disable prompting of players
        size = self.app.menu_screen.size
        self.app.start_game(game, size, demo=True)
        yield(1.2) # Compensating for .7 wait at start?!

        ps = self.app.pente_screen

        def mm(x,y):
            game.make_move((x,y))
            self.app.pente_screen.perform(0)
            self.app.pente_screen.refresh_all()

        play_speech("black_first")
        yield(2)

        play_speech("centre_first")
        yield(1.5)
        mm(3,4)
        yield(1)

        mm(6,8)
        yield(.5)
        mm(4,4)
        yield(.5)

        mm(6,7)
        yield(.5)
        mm(5,8)
        yield(.5)
        play_speech("line_5_wins")

        mm(6,9)
        yield(.5)
        mm(8,3)
        yield(.5)

        mm(6,10)
        yield(4)

        # Diagonal white win
        app.pente_screen.set_review_mode(False)
        game.go_to_the_beginning()
        yield(2)

        mm(6, 6)
        yield(.5)
        mm(5, 5)
        yield(.5)

        mm(4, 6)
        yield(.5)
        mm(7, 3)
        yield(.5)

        play_speech("diagonal_wins")

        mm(7, 5)
        yield(.5)
        mm(9, 1)
        yield(.5)

        mm(5, 6)
        yield(.5)
        mm(6, 4)
        yield(.5)

        mm(8, 6)
        yield(.8)
        mm(8, 2)
        yield(3.5)

        # Captures
        app.pente_screen.set_review_mode(False)
        game.go_to_the_beginning()
        yield(1)

        mm(6, 6)
        yield(.5)
        mm(6, 7)
        yield(.5)

        play_speech("pair_captures")

        mm(6, 5)
        yield(1.5)
        mm(6, 4)
        yield(2.5)
        
        mm(5, 3)
        yield(.5)
        mm(7, 5)
        yield(1)

        play_speech("diag_capt")
        yield(1.5)

        mm(8, 6)
        yield(2.5)
        mm(6, 6)
        yield(1)

        # Non captures
        ##############
        game.go_to_the_beginning()
        play_speech("non_capt")
        yield(2)

        # Length 1
        mm(0, 0)
        yield(.5)
        play_speech("single_stone")

        mm(0, 1)
        yield(1)
        mm(0, 2)
        yield(1)

        # Length 3
        mm(2, 1)
        yield(.5)
        mm(2, 0)
        yield(.5)
        play_speech("3_or_more")

        mm(2, 3)
        yield(.5)
        mm(8, 4)
        yield(.5)

        mm(2, 2)
        yield(1)
        mm(2, 4)
        yield(2)

        # Place inside the border
        mm(4, 1)
        yield(.5)
        mm(4, 0)
        yield(.5)

        play_speech("trigger_capt")

        mm(4, 10)
        yield(.5)
        mm(4, 3)
        yield(2)

        mm(4, 2) # Black places a piece inside, doesn't get taken
        yield(3)
        mm(6, 6)
        yield(1)

        # Gap
        play_speech("no_gaps")

        mm(6, 3)
        yield(.5)
        mm(6, 0)
        yield(.5)

        mm(6, 1)
        yield(1)
        mm(6, 4)
        yield(3)

        # Double capture
        mm(7, 6)
        yield(.5)

        play_speech("two_pairs")
        mm(5, 6)
        yield(.5)
        mm(7, 9)
        yield(.5)
        mm(5, 7)
        yield(.5)
        mm(0, 12)
        yield(.5)
        mm(6, 8)
        yield(.5)
        mm(4, 6)
        yield(3)

        # 5 Pairs win the game
        game.go_to_the_beginning()
        play_speech("capt_win")
        yield(1)

        # 1
        mm(0, 1)
        yield(.3)
        mm(0, 0)
        yield(.3)

        mm(0, 2)
        yield(.3)
        mm(0, 3)
        yield(.3)

        # 2
        mm(2, 1)
        yield(.3)
        mm(2, 0)
        yield(.3)

        mm(2, 2)
        yield(.3)
        mm(2, 3)
        yield(.3)

        # 3
        mm(4, 2)
        yield(.3)
        mm(4, 3)
        yield(.3)

        mm(4, 1)
        yield(.3)
        mm(4, 0)
        yield(.3)

        # 4
        mm(7, 1)
        yield(.3)
        mm(6, 0)
        yield(.3)

        mm(8, 2)
        yield(.3)
        mm(9, 3)
        yield(.3)

        # 5
        mm(2, 10)
        yield(.3)
        mm(0, 12)
        yield(.3)

        mm(1, 11)
        yield(2)
        mm(3, 9)
        yield(0.5)
        play_speech("capt_no_win")
        yield(5)

        # Demonstrate review mode
        play_speech("review")

        # Click go to beginning
        beginning_button = ps.panel_buttons.ids.beginning_id
        sim_press(beginning_button)

        yield(.3)

        game.go_to_the_beginning()
        yield(.7)

        # Click forward a few times
        forward_button = ps.panel_buttons.ids.forward_id
        for i in range(8):
            sim_press(forward_button)
            yield(.2)

            game.go_forwards_one()
            yield(.5)

        yield(4)

        ########


