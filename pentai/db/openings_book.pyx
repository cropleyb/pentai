import os

from pentai.base.defines import *
from pentai.base.pente_exceptions import *
import pentai.base.game as g_m
import pentai.db.zodb_dict as z_m
import pentai.ai.standardise as st_m
import pentai.db.preserved_game as pg_m
import pentai.db.op_pos as op_m
import pentai.base.logger as log

from BTrees.OOBTree import OOBTree

ZM = z_m.ZM
ZL = z_m.ZL

instance = None

OPENINGS_DEPTH = 10

def circulate(a):
    if len(a) > 10:
        a.extend(a[:10])
        a[:10] = []
    return a

class OpeningsBook(object):
    def __init__(self):
        self.turns_sections = z_m.get_section("openings")
        self.opening_game_ids = z_m.get_section("openings_games")

        global instance
        instance = self

    def get_subsection_name(self, move_number):
        return "move%s" % move_number

    def get_position_data(self, move_number, position):
        ssn = self.get_subsection_name(move_number)
        try:
            td = self.turns_sections[ssn]
        except KeyError:
            if move_number < 3:
                td = self.turns_sections[ssn] = ZM({})
            else:
                td = self.turns_sections[ssn] = OOBTree()
        pd = self.turns_sections[position] 
        return pd

    def add_game(self, g, won_by):
        if won_by == EMPTY:
            return

        if not g.get_size() in (13, 19):
            return

        if g.key() in self.opening_game_ids:
            raise OpeningsBookDuplicateException()
        self.opening_game_ids[g.key()] = True

        # Set the game as unfinished to game_state from raising exceptions
        # when we try to replay the game?! (TODO: Why is this special?)
        g.current_state._won_by = EMPTY

        max_moves = min(OPENINGS_DEPTH, len(g.move_history))
        for mn in range(1, 1+max_moves):
            # TODO: Limit the number of moves into the game.
            self.add_position(g, mn, won_by)

    def add_position(self, game, move_number, won_by):
        game.go_to_move(move_number)

        std_state, fwd, rev = st_m.standardise(game.current_state)
        position_key = std_state

        # Get the appropriate section for this position
        log.debug("add_position %s" % (position_key,))

        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        size = game.get_size()
        x, y = standardised_move
        if x < 0 or y < 0 or x >= size or y >= size:
            # Off the board - it's probably one of those suicide moves
            # to finish the game sooner
            return

        # TODO: Cache this somehow?
        rules = game.get_rules()
        rt = rules.type_char
        size = rules.size
        colour = game.to_move_colour()
        move_rating = game.get_rating(colour)

        try:
            pos_data = self.get_position_data(move_number, std_state)
        except KeyError:
            pos_data = self.turns_sections[std_state] = op_m.OpeningPos()

        pos_data.add_move(rt, size, standardised_move, won_by, move_rating)

    def safe_move(self, pos, our_game, size):
        x, y = pos

        if size <= our_game.size():
            return True

        safe_min_size = 4
        safe_max_size = our_game.size() - 5

        # Suggested move may be too near an edge
        return (x >= safe_min_size and y >= safe_min_size and \
                x <= safe_max_size and y <= safe_max_size)

    def filter_out_by_rules(self, search_game, move):
        rules = search_game.get_rules()
        return not rules.ok_third_move(move)

    def get_move_games(self, search_game):
        std_state, fwd, rev = st_m.standardise(search_game.current_state)
        log.debug("get_move_games: %s" % (std_state,))

        position_key = std_state

        turn_number = search_game.get_move_number()
        try:
            log.debug("looking in %s" % (position_key,))
            opening_pos = self.get_position_data(turn_number, position_key)
        except KeyError:
            return

        option_count = 0

        aip = search_game.get_current_player()
        ai_rating = aip.get_rating()
        search_rules = search_game.get_rules()

        # Don't use other sizes for now, they seem to give dodgy results
        search_size = search_rules.size
        sizes = [search_size]

        # Iterate over rules_type next (same, others)
        rules_types = ['s', 't', '5']
        search_rules_type = search_rules.type_char
        rules_types.remove(search_rules_type) # Move to front
        rules_types[:0] = [search_rules_type]

        if turn_number == 3:
            if search_rules_type == 's':
                # Don't use tournament rules moves
                rules_types.remove('t')
            elif search_rules_type == 't':
                # *Only* use tournament rules moves
                rules_types = ['t']

        for size in sizes:
            for rt in rules_types:
                if not search_game.is_live():
                    log.info("Interrupted openings book get_move_games")
                    return

                # iterate over moves and their stored data
                moves_data = opening_pos.get_moves_strict(rt, size)
                if not moves_data:
                    continue

                # circulate() TODO: shuffling of moves

                for move_data in moves_data.iteritems():
                    canonised_move, data = move_data

                    # De-canonize the suggested move
                    suggested_move = rev(*canonised_move)

                    # Where should this filtering be done?
                    move_rating = data.get_max_rating()
                    if move_rating < (ai_rating - 100):
                        log.debug("Potential move max rating %d is too low for AI %d" % 
                                (move_rating, ai_rating))
                        continue
                    if not self.safe_move(suggested_move, search_game, size):
                        continue

                    secondary = (search_rules_type != rt)

                    log.debug("secondary: %s" % secondary)
                    yield (suggested_move, data, secondary)
                    option_count += 1
                    if option_count > 10:
                        log.info("Enough opening options found")
                        return

    def after_game_won(self, game, colour):
        # Add the game to the openings library if req.
        # (i.e. we're subscribed)
        self.add_game(game)

