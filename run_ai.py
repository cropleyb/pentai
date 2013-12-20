#!/usr/bin/env python

import gui
import human_player
import rules
import game

import time

from ai_player import *

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
        return "Black time: %.2fs, White time: %.2fs" % tuple(self.totals)

class Genome():
    """
    max_depth
    width (max_moves_per_depth_level)
    narrowing: 0, 1, .5, -0.5 (per depth level)
    line base
    capture_score_base
    take_score_base
    threat_score_base
    capture scaling
    line length scaling
    the value of the move
    max_time_per_move (proportion of remaining time)
    total game time
    search iterations - 0,1,2,3
    """


class Match():
    def set_up(self):
        self.p1 = AIPlayer("Black")
        self.p2 = AIPlayer("White")
        r = rules.Rules(13, "standard")
        self.game = game.Game(r, self.p1, self.p2)

    # !./t_ai_player.py AIPlayerSubsystemTest.test_find_one_move
    def play_one_game(self):
        self.p1.set_max_depth(6)
        self.p1.set_max_moves_per_depth_level(9, narrowing=False)
        self.p2.set_max_depth(8)
        self.p2.set_max_moves_per_depth_level(6, narrowing=False)
        #self.p2.set_max_moves_per_depth_level(7)
        tt = TwoTimer()

        while not self.game.finished():
            p = self.game.get_current_player()
            with tt:
                m = p.do_the_search()
                self.game.make_move(m)
        print "Game was won by: %s" % self.game.winner_name()
        print tt


if __name__ == "__main__":
    m = Match()
    m.set_up()
    m.play_one_game()