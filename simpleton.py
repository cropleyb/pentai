import ab_bridge
import alpha_beta
from gui import *
import search_order
import board

from player import *

class SimpletonPlayer(Player):
    """ Yes there is a circular dependancy between SimpletonPlayer and Game """

    def __init__(self, name, colour):
        Player.__init__(self, name, colour)
        self.max_depth = 1

    def prompt_for_action(self, base_game, gui):
        # Take the first available empty position, nearest to the centre ;)
        pos_iter = search_order.PosIterator(base_game.size())
        board = base_game.get_board()
        for p in pos_iter.get_iter():
            if board.get_occ(p) == EMPTY:
                self.action = MoveAction(p)
                return

    def get_action(self, game, gui):
        # TODO: make move chosen by the search
        return self.action
