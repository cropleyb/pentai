
#!/usr/bin/env python

import unittest
from game import *
from preserved_game import *
from ai_factory import *
from players_mgr import * # TODO remove dependance, use mock

import pdb

class PreservedGameTest(unittest.TestCase):
    def setUp(self):
        self.test_players_fn = 'test_players.pkl'
        self.aif = AIFactory()

    def tearDown(self):
        try:
            os.unlink(self.test_players_fn)
        except OSError: pass

    def create_player(self, genome):
        return self.aif.create_player(genome)

    def test_preserve_game(self):
        genome1 = AIGenome("Sonia")
        p1 = self.create_player(genome1)
        genome2 = AIGenome("Toby")
        p2 = self.create_player(genome2)

        r = rules.Rules(13, "standard")
        orig_game = Game(r, p1, p2)
        orig_game.game_id = ((13, 's'), 1)
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
        genome1 = AIGenome("Marjory")
        genome1.chokes = [(4,3),(5,1)]
        p1 = self.create_player(genome1)
        genome2 = AIGenome("Hubert")
        p2 = self.create_player(genome2)

        ai_db = PlayersMgr(prefix="test_")
        ai_db.add(p1)
        ai_db.add(p2)

        pg = PreservedGame()
        pg.players = [None, "Marjory", "Hubert"]

        pg.rules = (9, 'f')
        pg.game_id = ((9, 'f'), 1)

        pg.moves = [(8,1)]
        pg.winner = BLACK

        today = datetime.date.today()
        pg.date = today

        orig_game = pg.restore(ai_db)

        self.assertEquals(orig_game.rules.key(), (9, 'f'))

        today = datetime.date.today()
        self.assertEquals(orig_game.date, today)

        self.assertEquals(len(orig_game.move_history), 1)
        self.assertEquals(orig_game.move_history[0], (8,1))

        self.assertEquals(orig_game.winner(), BLACK)

        black_player = orig_game.player[BLACK]
        self.assertEquals(black_player, p1)

        white_player = orig_game.player[WHITE]
        self.assertEquals(white_player, p2)

    # TODO: Test restore of human player

if __name__ == "__main__":
    unittest.main()

