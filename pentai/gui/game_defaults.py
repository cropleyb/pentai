from persistent import *
from pentai.base.defines import *
from pentai.db.zodb_dict import ZL

class GameDefaults(Persistent):
    def __init__(self, *args, **kwargs):
        super(GameDefaults, self).__init__(*args, **kwargs)
        self.last_game_types = ZL([None, None, None])
        self.last_game_players = ZL([None, "", ""])

        self.old_game_players_by_type_then_colour = ZL( [ZL([]), ZL([]), ZL([]) ])

        self.types = ZL([None, None, None])
        self.rules = None
        self.last_player_set_of_type_was_colour = ZL([None, None])

    def play_game(self, p1, p2, rules):
        self.rules = rules
        self.last_game_types[:] = ZL([None, p1[0], p2[0]])
        self.last_game_players[:] = ZL([None, p1[1], p2[1]])
        self.types = self.last_game_types[:]

        self.set_player(P1, p1[1])
        self.set_player(P2, p2[1])

    def add_game(self, game):
        p1, p2 = game.get_all_players()[1:]
        rules = game.get_rules()
        self.play_game((p1.get_type(), p1.get_name()), 
                        (p2.get_type(), p2.get_name()), rules)

    def get_size(self):
        try:
            return self.rules.size
        except AttributeError:
            return 19

    def get_rules_type_name(self):
        try:
            return self.rules.get_type_name()
        except AttributeError:
            return "Standard"

    def get_total_time(self):
        try:
            return self.rules.get_time_control()
        except AttributeError:
            return 0

    def get_player(self, colour):
        ret = self.get_player_inner(colour)
        return ret

    def get_player_inner(self, colour):
        # find the first unused name in the old games list for that type
        lookup_type = self.types[colour]
        ind = lookup_type == "Human"
        st_var = self.old_game_players_by_type_then_colour[ind]

        try:
            oc = opposite_colour(colour)
            if (self.types[oc] == lookup_type):
                # Two the same type

                was_last_set = \
                        self.last_player_set_of_type_was_colour[ind] == colour

                return st_var[not was_last_set]
        except IndexError:
            pass

        try:
            return st_var[0]
        except IndexError:
            return ""

    def get_type(self, colour):
        return self.types[colour]

    def get_player_type(self, colour):
        pt = self.types[colour]
        if pt == "AI":
            pt = "Computer"
        return pt

    def set_player(self, colour, name):
        self.last_game_players[colour] = name
        self.last_game_types[colour] = self.types[colour]

        type_name = self.get_type(colour)
        lookup_type = self.types[colour]

        ind = lookup_type == "Human"
        self.last_player_set_of_type_was_colour[ind] = colour

        st_var = self.old_game_players_by_type_then_colour[ind]

        try:
            if not name == st_var[0]:
                # push a new player name 
                st_var[:0] = ZL([name])
                st_var[2:] = ZL([])
        except IndexError:
            st_var.append(name)

    def set_type(self, colour, new_type):
        if self.types[colour] != new_type:
            self.types[colour] = new_type
