#!/usr/bin/env python

import unittest
#import sys

from pentai.base.rules import *
from pentai.base.game import *
from pentai.base.player import *
import pentai.db.test_db as tdb_m
import op_pos as op_m

class O_PosTest(unittest.TestCase):
    def setUp(self):
        tdb_m.init()
        self.rules = Rules(19, "standard")
        self.p1 = Player("BC")
        self.p2 = Player("Whoever")
        self.game = Game(self.rules, self.p1, self.p2)

    def tearDown(self):
        tdb_m.clear_all()
        tdb_m.delete_test_db()

    def test_empty_pos(self):
        o_pos = op_m.OpeningPosData()
        
        self.assertEquals(len(o_pos.get_moves()), 0)

    def test_add_move(self):
        o_pos = op_m.OpeningPosData()
        o_pos.add_move((7,7), BLACK, 1800)
        
        self.assertEquals(len(o_pos.get_moves()), 1)
        move, data = list(o_pos.get_moves().iteritems())[0]
        self.assertEquals(move, (7,7))
        self.assertEquals(data.get_wins(BLACK), 1)
        self.assertEquals(data.get_wins(WHITE), 0)
        self.assertEquals(data.get_avg_rating(), 1800)
        self.assertEquals(data.get_max_rating(), 1800)

    def test_add_more_moves(self):
        o_pos = op_m.OpeningPosData()
        o_pos.add_move((7,7), BLACK, 1800)
        o_pos.add_move((6,6), WHITE, 1300)
        o_pos.add_move((7,7), WHITE, 1500)
        
        self.assertEquals(len(o_pos.get_moves()), 2)
        move_data = sorted(list(o_pos.get_moves().iteritems()))

        move1, data1 = move_data[0]
        self.assertEquals(move1, (6,6))
        self.assertEquals(data1.get_wins(BLACK), 0)
        self.assertEquals(data1.get_wins(WHITE), 1)
        self.assertEquals(data1.get_avg_rating(), 1300)
        self.assertEquals(data1.get_max_rating(), 1300)

        move2, data2 = move_data[1]
        self.assertEquals(move2, (7,7))
        self.assertEquals(data2.get_wins(BLACK), 1)
        self.assertEquals(data2.get_wins(WHITE), 1)
        self.assertEquals(data2.get_avg_rating(), 1650)
        self.assertEquals(data2.get_max_rating(), 1800)

if __name__ == "__main__":
    unittest.main()

