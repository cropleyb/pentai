from pente_exceptions import *
from defines import *

class Rules():
    def __init__(self, *args, **kwargs):
        self.set_all(*args, **kwargs)

    def set_all(self, size, type_str, time_control=0):
        if size < 5:
            raise BoardTooSmallException()
        if size > 19:
            raise BoardTooBigException()
        self.size = size
        self.time_control = time_control * 60
        self.type_char = type_str.lower()[0]
        tc = self.type_char
        if tc == 's': # "standard"
            # TODO: constrain second black move attr.
            self.center_first = True
            self.stones_for_capture_win = 10
            self.can_capture_pairs = True
            self.can_capture_threes = False
            self.exactly_five = False
            self.border_colour = (0.83,0.83,0.83,1)
        elif tc == 't': # "tournament"
            self.center_first = True
            self.stones_for_capture_win = 10
            self.can_capture_pairs = True
            self.can_capture_threes = False
            self.exactly_five = False
            self.border_colour = (0.25,0.30,0.60,1)
        elif tc[:5] == 'k': # "keryo"
            self.center_first = True
            self.stones_for_capture_win = 15
            self.can_capture_pairs = True
            self.can_capture_threes = True
            self.exactly_five = False
            self.border_colour = (0.45,0.15,0.40,1)
        elif tc == 'f': # "freestyle"
            self.center_first = False
            self.stones_for_capture_win = 10
            self.can_capture_pairs = True
            self.can_capture_threes = False
            self.exactly_five = False
            self.border_colour = (0.03,0.43,0.30,1)
        elif tc == '5': # "five in a row"
            self.center_first = False
            self.stones_for_capture_win = 0 # can capture, but wins are only from 5
            self.can_capture_pairs = True
            self.can_capture_threes = False
            self.exactly_five = True
            self.border_colour = (0.48,0.08,0.08,1)
        elif tc == 'n': # captures
            self.center_first = False
            self.stones_for_capture_win = 0
            self.can_capture_pairs = False
            self.can_capture_threes = False
            self.exactly_five = False
            self.border_colour = (0.90,0.81,0.11,1)
        else:
            raise UnknownRuleType("%s, %s" % (size, type_str))

    def key(self):
        return (self.size, self.type_char)

    def __hash__(self):
        return hash(self.key())
     
    types = {'s': "Standard",
             't': "Tournament",
             'k': "Keryo-Pente",
             'f': "Freestyle",
             '5': "5-In-A-Row",
             'n': "No Capture"
             }

    def get_type_name(self):
        return self.types[self.type_char]

'''
    Standard rules
    First player must move on the center point - all subsequent moves are open. pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Tournament rules
    First player must move on the center point. First player's second move must be 3 or more points removed from the center point. pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Keryo-Pente rules
    First player must move on the center point - all subsequent moves are open. Using these rules three of your opponent's stones in a row can be captured, just like pairs. pairs can also be captured. Win by capturing 15 or more of your opponents stones (compared to the usual 5 pairs, which is 10 stones), OR by placing 5 or more stones in a row.
     
    Freestyle rules
    Stones may be placed anywhere on the board, including the first player's first move. pairs can be captured. Win by placing 5 or more stones in a row, OR by capturing 5 or more pairs of the opponent's stones.
     
    Five-In-A-Row rules
    Stones may be placed anywhere on the board, including the first player's first move. pairs can be captured, but don't count towards a win. Win ONLY by placing 5 or more stones in a row.
     
    No Capture rules
    Stones may be placed anywhere on the board, including the first player's first move. pairs can NOT be captured. Win ONLY by placing 5 or more stones in a row.
'''
