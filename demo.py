from kivy.clock import Clock

import time

from defines import *

import ai_genome as aig_m
import ai_factory as f_m
import human_player as h_m
import rules as r_m
import game as g_m

class Demo():
    def __init__(self, app, size):
        self.app = app
        self.size = size

        # TODO Save settings

        # TODO Save current game

        # TODO Intercept Input

        # Disable prompting of players

        self.script = self.rules_script()

    def play(self, dt=None):
        print "A"
        '''
        for i in range(20):
            now = time.time()
        '''

        try:
            print "B"
            sleep_time = self.script.next()
            print "C"
        except StopIteration:
            print "D"
            self.finish()
            return

        print "E"
        if sleep_time != None:
            print "F, %s" % sleep_time
            Clock.schedule_once(self.play, sleep_time)
            print "G"

    def finish(self):
        self.app.show_menu_screen()

    def rules_script(self):
        '''
        self.app.show_menu_screen()
        yield(2)
        '''
        #self.app.menu_screen.ids.new_game.state = "down"
        #yield(1)
        #self.app.menu_screen.ids.new_game.state = "normal"
        #yield(1)

        self.app.show_new_game_screen()
        yield(2)

        p1 = h_m.HumanPlayer("Bruce") # TODO: Use most recent human player name
        aif = f_m.AIFactory()
        genome = aig_m.AIGenome("PentAI")
        genome.use_openings_book = False
        p2 = aif.create_player(genome)

        # Create a game
        r = r_m.Rules(13, "standard")
        game = g_m.Game(r, p1, p2)

        yield(2)
        # And start it...
        #st()
        self.app.start_game(game, [457, 720], demo=True) # HACK
        #st()
        print "1a"
        yield(.5)
        print "1b"
        '''
        yield(.5)
        print "1c"
        yield(.5)
        #yield(1.5)
        print "2"
        '''


        def mm(x,y):
            game.make_move((x,y))
            self.app.pente_screen.perform(0)
            self.app.pente_screen.refresh_all()
        print "3"

        mm(3,4)
        print "4"
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
        mm(4, 0)
        yield(.5)

        mm(4, 1)
        yield(.5)
        mm(4, 3)
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

