
from game_state import *
from player import *
from rules import *

import datetime

class Game():

    def __init__(self, rules=None, player1=None, player2=None):
        self.rules = rules
        if rules != None:
            self.current_state = GameState(self)

        self.player = [None, player1, player2]
        if player1 != None:
            player1.attach_to_game(self)
        if player2 != None:
            player2.attach_to_game(self)
        self.move_history = []
        self.autosave = False

    # TODO: get_size for consistency
    def size(self):
        return self.rules.size

    def get_current_state(self):
        return self.current_state

    def get_board(self):
        return self.current_state.board

    def off_board(self, pos):
        return self.get_board().off_board(pos)

    def get_player(self, player_number):
        return self.player[player_number]
    
    def get_player_name(self, player_number):
        return self.player[player_number].get_name()

    def get_current_player(self):
        return self.current_state.to_move_player()

    def to_move_colour(self):
        return self.current_state.to_move_colour()

    def prompt_for_action(self, gui):
        if self.finished():
            return "Game was won by: %s" % self.winner_name()
        return self.get_current_player().prompt_for_action(self, gui)

    def get_action(self, gui):
        return self.get_current_player().get_action(self, gui)

    # Not sure if these should even delegate
    def get_move_number(self):
        return self.current_state.get_move_number()

    def set_move_number(self, turn):
        self.current_state.set_move_number(turn)

    def get_captured(self, player_number):
        return self.current_state.get_captured(player_number)

    def set_captured(self, player_number, pieces):
        return self.current_state.set_captured(player_number, pieces)

    def make_move(self, move):
        # Record this, then save to a file if required
        self.move_history = self.move_history[:self.get_move_number()-1]
        self.current_state.make_move(move)
        self.move_history.append(move)
        if self.autosave:
            self.save_history()

    def finished(self):
        return self.current_state.get_won_by() > 0

    def winner(self):
        return self.current_state.get_won_by()

    def winner_name(self):
        return self.player[self.current_state.get_won_by()-1]

    def get_move(self, move_number):
        return self.move_history[move_number-1]

    def go_forwards_one(self):
        self.go_to_move(self.get_move_number() + 1)

    def go_backwards_one(self):
        self.go_to_move(self.get_move_number() - 1)

    def go_to_move(self, move_number):
        current_move = self.get_move_number()
        if move_number < current_move:
            # Have to go back to the start, and replay all the moves,
            # otherwise the GUI and AI would need to support undo. TODO?
            gs = self.current_state
            gs.reset(self)

            for i in range(move_number-1):
                gs.make_move(self.move_history[i])
        else:
            for i in range(current_move-1, move_number-1):
                if i > len(self.move_history) - 1:
                    return
                gs = self.current_state
                gs.make_move(self.move_history[i])

    def history_to_str(self):
        game_str = self.game_header()
        for i in range(len(self.move_history)):
            move = self.move_history[i]
            # TODO: Could be slow for very long games (n**2)
            game_str = game_str + "%s. %s\n" % (i+1, move)
        return game_str

    def save_history(self):
        game_str = self.history_to_str()
        filename = "games/%s_%s_%s.txt" % \
            (self.get_player_name(BLACK),
             self.get_player_name(WHITE),
             str(datetime.date.today()))
        game_file = open(filename, "w")
        game_file.write(game_str)
        game_file.close()

    def configure_from_str(self, s):
        player_line, size_line, rules_line, the_rest = s.split('\n', 3)

        # TODO: This is ugly - these values will be replaced shortly
        if self.player[BLACK] == None:
            self.player = [None, Player("Black"), Player("White")]
        if self.rules == None:
            self.rules = Rules(5,"standard")

        players = player_line.split(" versus ", 1)
        self.player[1].name = players[0]
        self.player[2].name = players[1]

        side_length, ignored = size_line.split('x', 1)
        self.rules.size = int(side_length)

        rules_type, ignored = rules_line.split(" rules", 1)
        self.rules.type_str = rules_type

        return the_rest

    def game_header(self):
        player_line = "%s versus %s" % \
                (self.get_player_name(1), self.get_player_name(2))
        size_line = "%sx%s"% (self.size(), self.size())
        rules_line = "%s rules\n" % self.rules.type_str
        return "\n".join([player_line, size_line, rules_line])

    def load_game(self, game_str):
        remainder = self.configure_from_str(game_str)
        self.load_moves(remainder)

    def load_moves(self, game_str):
        # e.g. "1. (4,4)\n2. (3,3)\n"
        #try:
            gs = game_str.strip()

            for line in gs.split('\n'):
                fields = line.split(' ', 1)
                move_number = int(fields[0][:-1])
                move_pos_tuple = fields[1]
                move_pos_str = move_pos_tuple[1:-1]
                coords = move_pos_str.split(',')
                move = int(coords[0]), int(coords[1])
                self.make_move(move)
        #except:
        #    raise IncompatibleFileException("Could not read line: %s" % line)

