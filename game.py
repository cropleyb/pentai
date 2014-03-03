
from pente_exceptions import *

import game_state
import player # Shouldn't be necessary?
import rules
from defines import *

import datetime

class Game(object):

    def __init__(self, *args, **kwargs):
        self.game_id = None
        self.move_history = []
        self.time_history = []
        self.remaining_times = [None, 0, 0]
        self.resume_move_number = None
        self.date = datetime.date.today() # TODO
        self.setup(*args, **kwargs)

    def setup(self, rules=None, player1=None, player2=None):
        self.rules = rules
        if rules != None:
            self.current_state = game_state.GameState(self)

            total_time = rules.time_control
            if total_time:
                # B/W
                self.remaining_times[BLACK] = total_time
                self.remaining_times[WHITE] = total_time

        self.players = [None, player1, player2]
        if player1 != None:
            player1.attach_to_game(self)
        if player2 != None:
            player2.attach_to_game(self)
        self.autosave_filename = None

    def __eq__(self, other):
        if not other.__class__ is Game:
            return False
        return self.game_id == other.game_id

    def resume(self):
        """ Call this once all the observers are set up """
        if not self.resume_move_number is None:
            rmn = self.resume_move_number
            self.go_to_move(rmn)

    def get_date(self):
        return self.date

    def get_rules(self):
        return self.rules

    def get_game_id(self):
        return self.game_id

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
        return self.players[player_number]
    
    def get_all_players(self):
        return self.players
    
    def get_player_name(self, player_number):
        return self.players[player_number].get_name()

    def get_current_player(self):
        return self.current_state.to_move_player()

    def to_move_colour(self):
        return self.current_state.to_move_colour()

    # TODO: Move this out of game, it seems to be gui stuff
    def prompt_for_action(self, gui):
        if self.was_interrupted():
            return
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
        if len(self.move_history) > 0:
            self.move_history = self.move_history[:self.get_move_number()-1]
            self.time_history = self.time_history[:self.get_move_number()-1]
        self.move_history.append(move)
        colour = self.to_move_colour()
        self.time_history.append(self.remaining_time(colour))
        self.resume_move_number = len(self.move_history) + 1

        try:
            self.current_state.make_move(move)
        except IllegalMoveException, e:
            # Wipe that one off.
            self.move_history = self.move_history[:-1]
            raise e

        if self.autosave_filename != None:
            self.save_history()

    def set_won_by(self, colour):
        self.current_state.set_won_by(colour)

    def set_interrupted(self):
        self.set_won_by(BLACK + WHITE)
        self.players[BLACK].set_interrupted()
        self.players[WHITE].set_interrupted()

    def was_interrupted(self):
        # TODO: Also using this combo for draws
        return self.current_state.get_won_by() == BLACK + WHITE

    def finished(self):
        return self.current_state.get_won_by() > 0

    def get_won_by(self):
        return self.current_state.get_won_by()

    def status(self):
        won_by = self.current_state.get_won_by()
        ret = ["Unf.", "B", "W", "D"][won_by]
        return ret

    def winner_name(self):
        return self.players[self.current_state.get_won_by()]

    def get_move(self, move_number):
        return self.move_history[move_number-1]

    def go_to_the_beginning(self):
        self.go_to_move(1)

    def go_forwards_one(self):
        self.go_to_move(self.get_move_number() + 1)

    def go_backwards_one(self):
        self.go_to_move(self.get_move_number() - 1)
    
    def go_to_the_end(self):
        self.go_to_move(len(self.move_history)+1)

    def go_to_move(self, move_number):
        # TODO: All these +1 and -1 shifts look a bit dodgy.
        current_move = self.get_move_number()
        self.resume_move_number = move_number
        time_hist = self.time_history[:]

        if move_number < current_move:
            # Have to go back to the start, and replay all the moves,
            # otherwise the GUI and AI would need to support undo. TODO?
            gs = self.current_state
            gs.reset(self)

            total_time = self.rules.time_control
            self.remaining_times[BLACK] = total_time
            self.remaining_times[WHITE] = total_time

            for i in range(move_number-1):
                to_move_col = self.to_move_colour()
                self.remaining_times[to_move_col] = time_hist[i]

                gs.make_move(self.move_history[i])
        else:
            for i in range(current_move-1, move_number-1):
                if i > len(self.move_history) - 1:
                    return
                to_move_col = self.to_move_colour()
                self.remaining_times[to_move_col] = time_hist[i]

                gs = self.current_state
                gs.make_move(self.move_history[i])

        self.time_history = time_hist
        # If we go back to the beginning of the game,
        # there won't have been any save() calls, so we won't
        # be able to resume from the beginning of the game.
        # Not much point for this anyway.
        self.current_state.send_up_to_date()

    def history_to_str(self):
        """ Keep this for test code and debugging """
        game_str = self.game_header()
        for i in range(len(self.move_history)):
            move = self.move_history[i]
            # TODO: Could be slow for very long games (n**2)
            game_str = game_str + "%s. %s\n" % (i+1, move)
        return game_str

    def save_history(self):
        """ Keep this for test code and debugging """
        game_str = self.history_to_str()
        filename = self.autosave_filename
        game_file = open(filename, "w")
        # TODO: Append to the file
        game_file.write(game_str)
        game_file.close()

    def configure_from_str(self, s):
        """ Keep this for test code """
        player_line, size_line, rules_line, the_rest = s.split('\n', 3)

        # TODO: This is ugly - these values will be replaced shortly
        if self.players[BLACK] is None:
            self.players = [None, player.Player("Black"), player.Player("White")]
        if self.rules is None:
            self.rules = rules.Rules(5,"standard")

        players = player_line.split(" versus ", 1)
        self.players[1].p_name = players[0]
        self.players[2].p_name = players[1]

        side_length, ignored = size_line.split('x', 1)

        rules_type, ignored = rules_line.split(" rules", 1)
        size = int(side_length)
        self.rules.set_all(size, type_str=rules_type)

        return the_rest

    def game_header(self):
        """ Keep this for test code """
        player_line = "%s versus %s" % \
                (self.get_player_name(1), self.get_player_name(2))
        size_line = "%sx%s"% (self.size(), self.size())
        rules_line = "%s rules\n" % self.rules.get_type_name()
        return "\n".join([player_line, size_line, rules_line])

    def load_game(self, game_str):
        """ Keep this for test code """
        remainder = self.configure_from_str(game_str)
        self.load_moves(remainder)
        self.resume()

    def load_moves(self, game_str):
        """ Keep this for test code """
        # e.g. "1. (4,4)\n2. (3,3)\n"
        gs = game_str.strip()

        for line in gs.split('\n'):
            fields = line.split(' ', 1)
            move_number = int(fields[0][:-1])
            move_pos_tuple = fields[1]
            move_pos_str = move_pos_tuple[1:-1]
            coords = move_pos_str.split(',')
            move = int(coords[0]), int(coords[1])
            self.make_move(move) # TODO Maybe skip this?

    def get_total_time(self):
        return self.rules.time_control

    def tick(self, colour, seconds):
        self.remaining_times[colour] -= seconds
        remaining = self.remaining_times[colour]

        if remaining <= 0:
            self.set_won_by(opposite_colour(colour))
        return remaining

    def remaining_time(self, colour): # TODO: get_
        return self.remaining_times[colour]

    def set_remaining_time(self, colour, t):
        self.remaining_times[colour] = t

