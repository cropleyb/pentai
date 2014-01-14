
#!/usr/bin/env python

import unittest
from game import *
from priority_filter_2 import *
from ai_player import *
from rules import *
from preserved_game import *
from games_db import *

import pdb

class PreservedGameTest(unittest.TestCase):
    def setUp(self):
        pass

    def create_player(self, name, mmpdl, narrowing, chokes):
        sf = PriorityFilter2()
        return AIPlayer(sf, name=name)

    #    def create_game(self): TODO?

    def test_preserve_game(self):
        chokes = [] # TODO: Save AI players?!
        p1 = self.create_player("Sonia", 9, 0, chokes)
        p2 = self.create_player("Toby", 9, 0, chokes)

        r = Rules(13, "standard")
        orig_game = Game(r, p1, p2)
        orig_game.make_move((7,3))

        pg = PreservedGame(orig_game)
        self.assertEquals(pg.rules, (13, 's'))

        black_player = pg.players[BLACK]
        self.assertEquals(black_player, "Sonia")
        white_player = pg.players[WHITE]
        self.assertEquals(white_player, "Toby")

        today = datetime.date.today()
        self.assertEquals(pg.date, today)

        self.assertEquals(len(pg.moves), 1)
        self.assertEquals(pg.moves[0], (7,3))

        self.assertEquals(pg.winner, 0)

    def test_restore_game(self):
        chokes = [(4,3),(5,1)]
        pg = PreservedGame()
        pg.players = [None, "Marjory", "Hubert"]

        pg.rules = (9, 'f')
        pg.moves = [(8,1)]
        pg.winner = BLACK

        today = datetime.date.today()
        pg.date = today

        orig_game = pg.reincarnate()

        self.assertEquals(orig_game.rules.key(), (9, 'f'))

        today = datetime.date.today()
        self.assertEquals(orig_game.date, today)

        self.assertEquals(len(orig_game.move_history), 1)
        self.assertEquals(orig_game.move_history[0], (8,1))

        self.assertEquals(orig_game.winner, BLACK)

        black_player = orig_game.players[BLACK]
        self.assertEquals(black_player, "Marjory")
        white_player = orig_game.players[WHITE]
        self.assertEquals(white_player, "Hubert")

if __name__ == "__main__":
    unittest.main()

