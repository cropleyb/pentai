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
    def __init__(self, longarr):
        self.max_depth = longarr[0]
        self.mmpdl = longarr[1]
        self.narrowing = (longarr[2] - 2) / 2.0

class Match():
    def create_player(self, name, genome):
        p = AIPlayer(name=name, mmpdl=genome.mmpdl, narrowing=genome.narrowing)
        p.set_max_depth(genome.max_depth)
        p.set_max_moves_per_depth_level(genome.mmpdl, genome.narrowing)
        return p

    def set_up(self):
        genome1 = Genome([6, 9, 0])
        genome2 = Genome([6, 9, 0])
        self.p1 = self.create_player("Black", genome1)
        self.p2 = self.create_player("White", genome2)
        r = rules.Rules(13, "standard")
        self.game = game.Game(r, self.p1, self.p2)

    def play_one_game(self):
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
