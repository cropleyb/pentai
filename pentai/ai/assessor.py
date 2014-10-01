
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

class ValueWrapper(object):
    def __init__(self, v):
        self._val = v

    def __lt__(self, other):
        return self._val < other

'''
"Bad moves" can be identified by a stronger AI, or by strong players.
When a bad move is identified, I need to figure out why the actual move was
given a better score than the best move. This (usually?) depends on the utility
values that determined the chosen and best moves (from the AB search)
Do a search for each of those two moves, and show the utility stats for each
position. The Game State needs to be bubbled back to the top for each and printed, along with the move history
UI: Click to move in review mode, to show a search by the current player, with utility stats and move history of the deep minimax path leading to that move.
'''
