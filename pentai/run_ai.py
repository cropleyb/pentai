#!/usr/bin/env python
'''
from guppy import hpy
h = hpy()
h.setref()
'''

import pentai.base.rules as r_m
import pentai.base.game as g_m

import time

from pentai.ai.ai_player import *
#from pentai.db.evaluator import *
from pentai.db.ai_factory import *
from pentai.db.openings_book import *
from pentai.db.games_mgr import *
import pentai.db.zodb_dict as z_m

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
        self.openings_book = OpeningsBook()

    def set_up(self, game_length):
        aif = AIFactory()
        self.genome1.max_depth = game_length
        self.genome2.max_depth = game_length
        self.p1 = aif.create_player(self.genome1)
        self.p2 = aif.create_player(self.genome2)

    def play_one_game(self, board_size, rules_type, p1, p2):
        r = r_m.Rules(board_size, rules_type)
        self.game = self.games_mgr.create_game(r, p1, p2)
        #self.evaluator = Evaluator(self.game.current_state)

        tt = TwoTimer()

        while not self.game.finished():
            p = self.game.get_current_player()
            with tt:
                m = p.do_the_search()
                self.game.make_move(m)
                #print self.evaluator.utility()

        winner_name = self.game.winner_name()
        winner = self.game.get_won_by()

        if self.openings_book:
            self.openings_book.add_game(self.game, winner)
        
        if p1.get_name() == "Contender":
            ratio = tt.totals[0] / tt.totals[1]
        else:
            ratio = tt.totals[1] / tt.totals[0]

        print "Game was won by: %s %s" % (["?", "B", "W"][winner], winner_name)
        print tt
 
        return "%s vs. %s: %s (%sx%s %s) %s" % (p1.get_name(), p2.get_name(), winner_name,
                board_size, board_size, p1.max_depth, tt), winner, winner_name, ratio

    def play_some_games(self):

        self.genome1.use_openings_book = False
        #self.genome2.use_openings_book = False
        #self.genome2.use_net_captures = False

        #self.genome2.length_factor = 35
        #self.genome2.take_score_base = 70
        #self.genome2.capture_score_base = 350 # Try this again for high depth
        #self.genome2.threat_score_base = 25 # Wins more for shallower depth
        #self.genome1.enclosed_four_base = 300
        #self.genome2.enclosed_four_base = 500
        #self.genome1.vision = 0.98
        #self.genome2.vision = 0.98

        #self.genome2.filter_num = 3
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

        #self.genome2.calc_mode = 2
        #self.genome2.use_net_captures = False
        #self.genome2.scale_pob = True
        #self.genome2.move_factor = 50
        #self.genome2.move_factor = 45
        #self.genome2.move_factor = 5
        #self.genome2.force_depth = 4 FAIL ;)
        #self.genome2.misjudgement = 8

        results = MatchResults()
        for game_length in range(2,7):
        #for game_length in range(2,5):
        #for game_length in range(2,4):
            #for board_size in [13]:
            for board_size in [13, 19]:
                for first_player in [0, 1]:
                    for rules_type in ['s', 't']:
                        self.set_up(game_length)
                        players = [self.p1, self.p2]
                        second_player = 1 - first_player
                        res = self.play_one_game(board_size, rules_type,
                                                 players[first_player],
                                                 players[second_player])
                        #hits = [players[i].ab_game.transposition_hits for i in [0,1]]
                        #print "Hits: %s" % hits
                        results.add(res)

        print results

import sys

def memory_usage_resource():
    import resource
    rusage_denom = 1024.
    if sys.platform == 'darwin':
        # ... it seems that in OSX the output is different units ...
        rusage_denom = rusage_denom * rusage_denom
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
    return mem

import random
import pstats, cProfile

import gc

if __name__ == "__main__":
    z_m.set_db("db.fs")
     
    '''
    random.seed()
    # the code you want to memory-profile
    '''
      
    '''
    #while True:
    m = Match()
    m.play_some_games()
    m = None
    gc.collect()

    mem = memory_usage_resource()
    print mem
    '''
    '''
    heap_data = h.heap()
    print heap_data
    print heap_data.more
    st()
    '''
    m = Match()
    cProfile.runctx("m.play_some_games()", globals(), locals(), "Profile.prof")

    s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("cumulative").print_stats(20) # or "time"
    s.strip_dirs().sort_stats("time").print_stats(20)
