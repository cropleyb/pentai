import os

from pentai.base.defines import *
from pentai.base.pente_exceptions import *
import pentai.base.game as g_m
import pentai.db.zodb_dict as z_m
import pentai.ai.standardise as st_m
import pentai.db.preserved_game as pg_m
import pentai.db.op_pos as op_m

ZM = z_m.ZM
ZL = z_m.ZL

instance = None

OPENINGS_DEPTH = 8

def circulate(a):
    if len(a) > 10:
        a.extend(a[:10])
        a[:10] = []
    return a

class OpeningsBook(object):
    def __init__(self, games_mgr):
        self.games_mgr = games_mgr
        self.positions_dbs = z_m.get_section("openings")
        self.turns_sections = z_m.get_section("openings")

        global instance
        instance = self

    def get_subsection_name(self, move_number):
        return "move%s" % move_number

    def get_turn_data(self, move_number):
        ssn = self.get_subsection_name(move_number)
        try:
            f = self.turns_sections[ssn]
        except KeyError:
            f = self.turns_sections[ssn] = op_m.OpeningPos()
        return f

    def get_db(self, g):
        if g is None:
            return None
        fn = self.get_subsection_name(g)
        try:
            f = self.positions_dbs[fn]
        except KeyError:
            f = self.positions_dbs[fn] = z_m.get_section(fn)
        return f

    def add_game_new(self, g, won_by):
        if won_by == EMPTY:
            return

        # Set the game as unfinished to game_state from raising exceptions
        # when we try to replay the game?! (TODO: Why is this special?)
        g.current_state._won_by = EMPTY

        max_moves = min(OPENINGS_DEPTH, len(g.move_history))
        for mn in range(1, 1+max_moves):
            # TODO: Limit the number of moves into the game.
            self.add_position_new(g, mn, won_by)

    def add_position_new(self, game, move_number, won_by):
        game.go_to_move(move_number)

        std_state, fwd, rev = st_m.standardise(game.current_state)
        position_key = std_state

        # Get the appropriate section for this position
        log.debug("add_position %s" % (position_key,))

        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        if standardised_move[0] < 0 or standardised_move[1] < 0:
            # Off the board - it's probably one of those suicide moves
            # to finish the game sooner
            return

        # TODO: Cache this somehow?
        rules = game.get_rules()
        rt = rules.type_char
        size = rules.size
        colour = game.to_move_colour()
        move_rating = game.get_rating(colour)

        turn_data = self.get_turn_data(move_number)
        turn_data.add_move(rt, size, standardised_move, won_by, move_rating)

    def add_game(self, g, update_cache=True, sync=True):
        # Save the game first, before it is manipulated
        self.games_mgr.save(g, update_cache=update_cache)

        # Copy the game instance as this process munges the game.
        pm = self.games_mgr.players_mgr
        g = pg_m.PreservedGame(g).restore(pm)

        if not g.finished():
            # Only add finished games to the openings book
            return

        # Set the game as unfinished to game_state from raising exceptions
        # when we try to replay the game?! (TODO: Why is this special?)
        g.current_state._won_by = EMPTY

        max_moves = min(OPENINGS_DEPTH, len(g.move_history))
        for mn in range(1, 1+max_moves):
            # TODO: Limit the number of moves into the game.
            self.add_position(g, mn)
        if sync:
            z_m.sync()

    def add_position(self, game, move_number, sync=False):
        game.go_to_move(move_number)

        std_state, fwd, rev = st_m.standardise(game.current_state)
        position_key = std_state

        # Get the appropriate section for positions of this rule type and size
        db = self.get_db(game)
        log.debug("add_position %s" % (position_key,))
        pos_slot = db.setdefault(position_key, ZM())
        next_move = game.move_history[move_number-1]
        standardised_move = fwd(*next_move)
        if standardised_move[0] < 0 or standardised_move[1] < 0:
            # Off the board - it's probably one of those suicide moves
            # to finish the game sooner, don't store it.
            return

        arr = pos_slot.setdefault(standardised_move, ZL())
        if move_number == 1:
            # Should only be in there once per id
            if game.game_id in arr:
                raise OpeningsBookDuplicateException()
        arr.append(game.game_id)

        if sync:
            self.games_mgr.save(game)
            z_m.sync()
        return db

    def safe_move(self, pos, candidate_game, our_game):
        x, y = pos

        if candidate_game.get_size() <= our_game.size():
            return True

        safe_min_size = 4
        safe_max_size = our_game.size() - 5

        # Suggested move may be too near an edge
        return (x >= safe_min_size and y >= safe_min_size and \
                x <= safe_max_size and y <= safe_max_size)

    def filter_out_by_rules(self, search_game, move):
        rules = search_game.get_rules()
        return not rules.ok_third_move(move)

    def get_move_games_new(self, search_game):
        std_state, fwd, rev = st_m.standardise(search_game.current_state)
        log.debug("get_move_games: %s" % (std_state,))

        position_key = std_state

        turn_number = search_game.get_move_number()
        try:
            log.debug("looking in %s" % (position_key,))
            opening_pos = self.get_turn_data(turn_number)
        except KeyError:
            return

        option_count = 0

        aip = search_game.get_current_player()
        ai_rating = aip.get_rating()
        search_rules = search_game.get_rules()

        # Iterate over size first (same, other)
        sizes = [13, 19]
        search_size = search_rules.size
        sizes.remove(search_size) # Move to front
        sizes[:0] = [search_size]

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
                    log.info("Interrupted openings book get_move_games_new")
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

                    yield suggested_move, data
                    option_count += 1
                    if option_count > 10:
                        log.info("Enough opening options found")
                        return


    def get_move_games(self, search_game):
        position_key, fwd, rev = st_m.standardise(search_game.current_state)
        log.debug("get_move_games: %s" % (std_state,))

        db = self.get_db(search_game)

        options = {}
        try:
            log.debug("looking in %s" % (position_key,))
            pos_slot = db[position_key]
        except KeyError, e:
            return

        safe_min_size = 5
        safe_max_size = search_game.size() - 5

        option_count = 0

        move_number = search_game.get_move_number()
        aip = search_game.get_current_player()
        ai_rating = aip.get_rating()
        colour = search_game.to_move_colour()

        for pos, gids in pos_slot.iteritems():
            if not search_game.is_live():
                log.info("Interrupted opening book get move games")
                return

            # TODO: Some sort of LRU for pos_slot iteritems?!
            move = rev(*pos)

            games = []

            if move_number == 3:
                if self.filter_out_by_rules(search_game, move):
                    log.info("Filter out by move 3 rules")
                    continue

            # Convert the game_ids to games
            for gid in gids:
                pg = self.games_mgr.get_preserved_game(gid, update_cache=False)
                if pg:

                    if not self.safe_move(move, pg, search_game):
                        # Suggested move is too near an edge
                        log.debug("Unsafe move %s" % (move,))
                        continue

                    move_rating = pg.get_rating(colour)
                    if move_rating < (ai_rating - 300):
                        log.debug("Potential move rating %d is too low for AI %d" % 
                                (move_rating, ai_rating))
                        continue

                    games.append(pg)
                    if len(games) > 10:
                        # That'll do
                        break

            # Use different saved games next time
            circulate(gids)

            if len(games):
                yield move, games
                option_count += 1
                if option_count > 6:
                    log.info("Enough opening options found")
                    return

    def after_game_won(self, game, colour):
        # Add the game to the openings library if req.
        # (i.e. we're subscribed)
        self.add_game(game)

