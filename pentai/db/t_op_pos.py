#!/usr/bin/env python

import unittest

from pentai.base.rules import *
from pentai.base.game import *
from pentai.base.player import *
import pentai.db.test_db as tdb_m
import op_pos as op_m

class O_PosTest(unittest.TestCase):
    def test_empty_pos(self):
        o_pos = op_m.OpeningPosMoveData()
        
        self.assertEquals(len(o_pos), 0)

    def test_add_move(self):
        o_pos = op_m.OpeningPosMoveData()
        o_pos.add_move((7,7), P1, 1800)
        
        self.assertEquals(len(o_pos), 1)
        move, data = list(o_pos.iteritems())[0]
        self.assertEquals(move, (7,7))
        self.assertEquals(data.get_wins(P1), 1)
        self.assertEquals(data.get_wins(P2), 0)
        self.assertEquals(data.get_avg_rating(), 1800)
        self.assertEquals(data.get_max_rating(), 1800)

    def test_add_more_moves(self):
        o_pos = op_m.OpeningPosMoveData()
        o_pos.add_move((7,7), P1, 1800)
        o_pos.add_move((6,6), P2, 1300)
        o_pos.add_move((7,7), P2, 1500)
        
        self.assertEquals(len(o_pos), 2)
        move_data = sorted(list(o_pos.iteritems()))

        move1, data1 = move_data[0]
        self.assertEquals(move1, (6,6))
        self.assertEquals(data1.get_wins(P1), 0)
        self.assertEquals(data1.get_wins(P2), 1)
        self.assertEquals(data1.get_avg_rating(), 1300)
        self.assertEquals(data1.get_max_rating(), 1300)

        move2, data2 = move_data[1]
        self.assertEquals(move2, (7,7))
        self.assertEquals(data2.get_wins(P1), 1)
        self.assertEquals(data2.get_wins(P2), 1)
        self.assertEquals(data2.get_avg_rating(), 1650)
        self.assertEquals(data2.get_max_rating(), 1800)

class O_PosRulesTest(unittest.TestCase):

    def test_empty_pos(self):
        o_pos = op_m.OpeningPos()
        
        self.assertEquals(len(o_pos), 0)

    def test_add_move(self):
        o_pos = op_m.OpeningPos()
        o_pos.add_move('t', 19, (7,7), P1, 1800)
        
        self.assertEquals(len(o_pos), 1)

        opmd = o_pos.get_moves_strict('t', 19)
        self.assertNotEquals(opmd, None)
        opmd2 = o_pos.get_moves_strict('s', 19)
        self.assertEquals(opmd2, None)
        opmd3 = o_pos.get_moves_strict('t', 13)
        self.assertEquals(opmd3, None)

        move, data = list(opmd.iteritems())[0]
        self.assertEquals(move, (7,7))
        self.assertEquals(data.get_wins(P1), 1)
        self.assertEquals(data.get_wins(P2), 0)
        self.assertEquals(data.get_avg_rating(), 1800)
        self.assertEquals(data.get_max_rating(), 1800)

    def test_add_yet_more_moves(self):
        o_pos = op_m.OpeningPosMoveData()
        o_pos.add_move((7,7), P1, 1800)
        o_pos.add_move((6,6), P2, 1300)
        o_pos.add_move((7,7), P2, 1500)
        
        self.assertEquals(len(o_pos), 2)
        move_data = sorted(list(o_pos.iteritems()))

        move1, data1 = move_data[0]
        self.assertEquals(move1, (6,6))
        self.assertEquals(data1.get_wins(P1), 0)
        self.assertEquals(data1.get_wins(P2), 1)
        self.assertEquals(data1.get_avg_rating(), 1300)
        self.assertEquals(data1.get_max_rating(), 1300)

        move2, data2 = move_data[1]
        self.assertEquals(move2, (7,7))
        self.assertEquals(data2.get_wins(P1), 1)
        self.assertEquals(data2.get_wins(P2), 1)
        self.assertEquals(data2.get_avg_rating(), 1650)
        self.assertEquals(data2.get_max_rating(), 1800)

import misc_db as m_m
import zodb_dict as z_m

class O_PosPersistenceTest(unittest.TestCase):

    def setUp(self):
        tdb_m.init()
        self.misc_db = m_m.get_instance()

    def tearDown(self):
        tdb_m.clear_all()

    def test_add_omgd_to_db(self):
        omgd = op_m.OpeningMoveGamesData((5,4,9000,1000))
        
        self.misc_db["omgd"] = omgd
        z_m.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["omgd"], omgd)

    def test_add_omgd_to_db(self):
        opmd = op_m.OpeningPosMoveData()
        opmd.add_move((7,7), P1, 1800)
        
        self.misc_db["opmd"] = opmd
        z_m.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["opmd"], opmd)

    def test_add_op_to_db(self):
        op = op_m.OpeningPos()
        op.add_move('t', 19, (7,7), P1, 1800)
        
        self.misc_db["op"] = op
        z_m.sync()
        mdb2 = m_m.get_instance()
        self.assertEquals(mdb2["op"], op)

if __name__ == "__main__":
    unittest.main()

