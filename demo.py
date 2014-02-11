from kivy.clock import Clock

import time

from defines import *

import ai_genome as aig_m
import ai_factory as f_m
import human_player as h_m
import rules as r_m
import game as g_m

def play_demo(app, size):
    d = Demo(app, size)
    d.play()

class Demo():

    def __init__(self, app, size):
        self.app = app
        self.size = size # TODO
        print "SIZE: " + str(size)

        # TODO Save settings

        # TODO Save current game

        # TODO Intercept Input

        # Disable prompting of players

        self.script = self.rules_script()
        self.play()

    def play(self, *args):
        print "play(): %s" % time.ctime()
        try:
            sleep_time = self.script.next()
        except StopIteration:
            print "Finished DEMO"
            return
        if sleep_time != None:
            print "Waiting %s" % sleep_time
            Clock.schedule_once(self.play, sleep_time)

    def rules_script(self):
        self.app.show_menu_screen()
        yield(10)
        self.app.show_new_game_screen()
        #yield()
        yield(1)
        yield(1)
        yield(1)
        #yield(1)
        #yield(1)
        #yield(1)
        #yield(1)

        aif = f_m.AIFactory()
        genome = aig_m.AIGenome("PentAI")
        genome.use_openings_book = False
        p1 = aif.create_player(genome)
        p2 = h_m.HumanPlayer("Bruce") # TODO: Use most recent human player name

        # Create a game
        r = r_m.Rules(13, "standard")
        game = g_m.Game(r, p1, p2)

        # And start it...
        #self.app.start_game(game, self.size)
        #yield(3)
        #yield(1)
        #time.sleep(.1)
        #st()
        self.app.start_game(game, [457, 720], demo=True) # HACK
        #self.app.start_game(game, [457, 720], demo=False) # HACK
        yield(1)
        #st()
        #time.sleep(.1)

        #def move(x, y):
        yield(1)
        #yield(1)
        #yield(1)
        def mm(x,y):
            game.make_move((x,y))
            self.app.pente_screen.perform(0)

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
        yield(.5)

        #yield(1)

