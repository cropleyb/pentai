
from pentai.base.defines import *
import pentai.db.ai_factory as aif_m # Hmmm. Shouldn't need to use this here
import pentai.ai.ai_genome as aig_m
import pentai.ai.ab_game as abg_m

class Assessor(object):
    def __init__(self, game):
        self.game = game.clone()
        self.game.set_live(True, gui=None)
        genome = aig_m.AIGenome("Assessor")
        genome.use_openings_book = False
        aif = aif_m.AIFactory()
        bp = self.best_player = aif.create_player(genome)
        self.ab_game = abg_m.ABGame(bp, self.game)
        #bp.set_max_depth(10)
        bp.set_max_depth(4) # TEMP for testing
        self.best_player.attach_to_game(self.game)
        self.game.resume()

    def set_turn_number(self, tn):
        self.game.go_to_move(tn)

    def calc_best_move(self, gui):
        answer = self.best_player.prompt_for_action(
                self.game, gui=gui, test=True)
        # TODO Ignore result in production - multithread
        turn, prev_move, move = answer
        return move
