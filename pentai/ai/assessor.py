
import pentai.db.ai_factory as aif_m # Hmmm. Shouldn't need to use this here
import pentai.ai.ai_genome as aig_m

class Assessor(object):
    def __init__(self, game):
        self.game = game.clone()
        genome = aig_m.AIGenome("Assessor")
        genome.use_openings_book = False
        aif = aif_m.AIFactory()
        bp = self.best_player = aif.create_player(genome)
        #bp.set_max_depth(10)
        bp.set_max_depth(4) # TEMP for testing
        self.best_player.attach_to_game(self.game)

    def set_turn_number(self, tn):
        self.game.go_to_move(tn)

    def calc_best_move(self, gui): # , test=False): TODO
        answer = self.best_player.prompt_for_action(
                self.game, gui=gui, test=True)
        return answer # Ignore in production
