
import pdb

from defines import *

class OpeningsDb():
    def __init__(self):
        self.games = {}
        self.positions = {}

    def get_games(self, rules):
        try:
            return self.games[rules]
        except KeyError:
            return []

    def add_game(self, g):
        rules = g.rules
        self.games.setdefault(rules, []).append(g)

    def add_position(self, game, move_number):
        game.go_to_move(move_number)

        # TODO convert to canonical form
        NE_strips = tuple(game.get_board().get_direction_strips()[0].strips)
        #pdb.set_trace()

        position_key = (NE_strips, game.get_captured(BLACK),
                    game.get_captured(WHITE))

        position_slot = self.positions.setdefault(position_key, [])
        next_move = game.move_history[move_number-1]
        position_slot.append((next_move, game))

    def get_moves(self, game):
        # TODO convert to canonical form, save the transformation
        NE_strips = tuple(game.get_board().get_direction_strips()[0].strips)

        position_key = (NE_strips, game.get_captured(BLACK),
                    game.get_captured(WHITE))

        #try:
        #pdb.set_trace()
        position_slot = self.positions[position_key]
        return position_slot
        #except KeyError:
            #return []

