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

class Demo():
    def __init__(self, app, size):
        self.app = app
        self.size = size

        # TODO Save settings
        # for settings demo

        # TODO Intercept Input

        self.script = self.rules_script()

    def start(self):
        self.app.root.set_demo_mode(True)
        self.play()

    def play(self, dt=None):
        try:
            sleep_time = self.script.next()
        except StopIteration:
            self.finish()
            return

        if sleep_time != None:
            sleep_time = (.8 + .4 * rand_m.random()) * sleep_time
            Clock.schedule_once(self.play, sleep_time)

    def finish(self):
        self.app.pente_screen = None
        self.app.show_menu_screen()
        self.app.root.set_demo_mode(False)

    def rules_script(self):
        # We're already on the menu screen
        app = self.app
        ms = app.menu_screen

        yield(1)
        ms.ids.new_game_id.sim_press()
        yield(.2)
        ms.ids.new_game_id.sim_release()

        app.show_new_game_screen()
        yield(.1)

        ss = app.setup_screen
        # TODO: Select white player type
        #ss.ids.white_type_id = "Computer"
        # TODO: Select computer player somehow?
        #ss.ids.wpl_id.text = "PentAI"

        yield(1)

        yield(1)
        ss.ids.start_game_id.sim_press()
        yield(.2)
        ss.ids.start_game_id.sim_release()

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

        #yield(2)
        # And start it...
        #st()

        # demo flag: Disable prompting of players
        self.app.start_game(game, [457, 720], demo=True) # size is a HACK
        yield(1.2) # Compensating for .7 wait at start?!

        def mm(x,y):
            game.make_move((x,y))
            self.app.pente_screen.perform(0)
            self.app.pente_screen.refresh_all()

        mm(3,4)
        yield(.5)

        mm(6,8)
        yield(.5)
        mm(4,4)
        yield(.5)

        mm(6,7)
        yield(.5)
        mm(5,8)
        yield(.5)

        mm(6,9)
        yield(.5)
        mm(8,3)
        yield(.5)

        mm(6,10)
        yield(5)

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

        mm(7, 5)
        yield(.5)
        mm(9, 1)
        yield(.5)

        mm(5, 6)
        yield(.5)
        mm(6, 4)
        yield(.5)

        mm(8, 6)
        yield(1)
        mm(8, 2)
        yield(5)

        # Captures
        app.pente_screen.set_review_mode(False)
        game.go_to_the_beginning()
        yield(2)

        mm(6, 6)
        yield(.5)
        mm(6, 7)
        yield(.5)

        mm(6, 5)
        yield(1.5)
        mm(6, 4)
        yield(2.5)
        
        mm(5, 3)
        yield(.5)
        mm(7, 5)
        yield(1.5)

        mm(8, 6)
        yield(1.5)
        mm(6, 6)
        yield(3)

        # Non captures
        ##############
        game.go_to_the_beginning()
        yield(2)

        # Length 1
        mm(6, 6)
        yield(.5)
        mm(0, 0)
        yield(.5)

        mm(0, 1)
        yield(1)
        mm(0, 2)
        yield(1)

        # Length 3
        mm(2, 1)
        yield(.5)
        mm(2, 0)
        yield(.5)

        mm(2, 3)
        yield(.5)
        mm(8, 4)
        yield(.5)

        mm(2, 2)
        yield(1)
        mm(2, 4)
        yield(3)

        # Place inside the border
        mm(4, 1)
        yield(.5)
        mm(4, 0)
        yield(.5)

        mm(4, 10)
        yield(.5)
        mm(4, 3)
        yield(2)

        mm(4, 2) # Black places inside, doesn't get taken
        yield(4)
        mm(9, 7)
        yield(1)

        # Gap
        mm(6, 3)
        yield(.5)
        mm(6, 0)
        yield(.5)

        mm(6, 1)
        yield(1)
        mm(6, 4)
        yield(5)

        # 5 Pairs wins
        game.go_to_the_beginning()
        yield(2)

        # 1
        mm(0, 1)
        yield(.5)
        mm(0, 0)
        yield(.5)

        mm(0, 2)
        yield(.5)
        mm(0, 3)
        yield(.5)

        # 2
        mm(2, 1)
        yield(.5)
        mm(2, 0)
        yield(.5)

        mm(2, 2)
        yield(.5)
        mm(2, 3)
        yield(.5)

        # 3
        mm(4, 2)
        yield(.5)
        mm(4, 3)
        yield(.5)

        mm(4, 1)
        yield(.5)
        mm(4, 0)
        yield(.5)

        # 4
        mm(7, 1)
        yield(.5)
        mm(6, 0)
        yield(.5)

        mm(8, 2)
        yield(.5)
        mm(9, 3)
        yield(.5)

        # 5
        mm(2, 10)
        yield(.5)
        mm(0, 12)
        yield(.5)

        mm(1, 11)
        yield(2)
        mm(3, 9)
        yield(4)

