#!/usr/bin/env python

import rules
import game

import time

from ai_player import *
from priority_filter import *
from priority_filter_2 import *
from blindness_filter import *
from evaluator import *
from ai_factory import *
from openings_book import *
from games_mgr import *

import pdb

class TwoTimer:
    def __init__(self):
        self.totals = [0.0, 0.0]
        self.current = 0

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.totals[self.current] += self.end - self.start
        self.current = 1 - self.current

    def __repr__(self):
        tot = self.totals
        return "B: %.2fs, W: %.2fs, B/W: %.2f" % (tot[0], tot[1], tot[0]/tot[1])

class MatchResults():
    def __init__(self):
        self.results = []
        self.bw_total = [0, 0, 0]
        self.dc_total = {"Defender":0, "Contender":0}
        self.total_ratio = 0.
        self.games_played = 0

    def __repr__(self):
        return "\n".join(self.results) + "\nB/W:" + str(self.bw_total) \
                + " won: " + str(self.dc_total) \
                + " C/D avg. time: " + str(self.total_ratio / self.games_played)

    def add(self, result):
        res_str, winner_colour, winner_name, ratio = result
        self.results.append(res_str)
        self.bw_total[winner_colour] += 1
        self.dc_total[str(winner_name)] += 1
        self.total_ratio += ratio
        self.games_played += 1

class Match():
    def __init__(self):
        self.genome1 = AIGenome("Defender")
        self.genome2 = AIGenome("Contender")
        # We're not doing player lookups, so we don't need the players_mgr
        self.games_mgr = GamesMgr()
        self.openings_book = OpeningsBook(self.games_mgr)

    def set_up(self, game_length):
        aif = AIFactory()
        self.genome1.max_depth = game_length
        self.genome2.max_depth = game_length
        self.p1 = aif.create_player(self.genome1)
        self.p2 = aif.create_player(self.genome2)

    def play_one_game(self, board_size, p1, p2):
        r = rules.Rules(board_size, "standard")
        self.game = self.games_mgr.create_game(r, p1, p2)
        #self.evaluator = Evaluator(UtilityCalculator(), self.game.current_state)

        tt = TwoTimer()

        while not self.game.finished():
            p = self.game.get_current_player()
            with tt:
                m = p.do_the_search()
                self.game.make_move(m)
                #print self.evaluator.utility()

        winner_name = self.game.winner_name()
        winner = self.game.get_won_by()

        self.openings_book.add_game(self.game)
        
        if p1.name == "Contender":
            ratio = tt.totals[0] / tt.totals[1]
        else:
            ratio = tt.totals[1] / tt.totals[0]

        print "Game was won by: %s %s" % (["?", "B", "W"][winner], winner_name)
        print tt
 
        return "%s vs. %s: %s (%sx%s %s) %s" % (p1.name, p2.name, winner_name,
                board_size, board_size, p1.max_depth, tt), winner, winner_name, ratio

    def play_some_games(self):

        self.genome1.use_openings_book = False
        self.genome2.use_openings_book = False
        #self.genome2.use_net_captures = False
        #self.genome2.length_factor = 40
        #self.genome2.take_score_base = 70
        #self.genome2.capture_score_base = 350 # Try this again for high depth
        #self.genome2.threat_score_base = 25 # Wins more for shallower depth
        #self.genome1.blindness = 0.02
        #self.genome2.blindness = 0.02

        #self.genome2.filter2 = True
        #self.genome2.narrowing = 3
        #self.genome2.max_depth += 2 # Setting max_depth here doesn't work
        #self.genome2.mmpdl = 15
        #self.genome1.chokes = []
        #self.genome2.chokes = [(4,5)]
        #self.genome2.chokes = [(4,3)]
        #self.genome2.chokes = [(2,2)]
        #self.genome1.max_depth_boost = 2
        #self.genome2.max_depth_boost = 2
        #self.genome2.captures_scale = [1, 1, 1, 1, 2, 4]
        #self.genome2.captures_scale = [0, 0, 0, 0, 0, 0]
        #self.genome2.length_scale = [0, 0, 0, 0, 0, 0]
        #self.genome2.move_factor = 10000000

        #self.genome1.calc_mode = 3
        #self.genome2.calc_mode = 3
        self.genome2.use_net_captures = True
        #self.genome2.move_factor = 50
        #self.genome2.move_factor = 45
        #self.genome2.move_factor = 5
        self.genome2.scale_pob = False

        results = MatchResults()
        for game_length in range(2,6):
        #for game_length in range(5,6):
        #for game_length in range(5,8):
            #for board_size in [13]:
            for board_size in [9, 13, 19]:
                for first_player in [0, 1]:
                    self.set_up(game_length)
                    players = [self.p1, self.p2]
                    second_player = 1 - first_player
                    res = self.play_one_game(board_size,
                                             players[first_player],
                                             players[second_player])
                    #hits = [players[i].ab_game.transposition_hits for i in [0,1]]
                    #print "Hits: %s" % hits
                    results.add(res)

        print results

import random
import pstats, cProfile

if __name__ == "__main__":
    random.seed()
    #while True:
    m = Match()
    m.play_some_games()
    '''
    m = Match()
    cProfile.runctx("m.play_some_games()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    s.strip_dirs().sort_stats("time").print_stats(20)
    '''
