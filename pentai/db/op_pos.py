from pentai.base.defines import *
from pentai.base.pente_exceptions import *
from pentai.db.zodb_dict import *

import array

class OpeningMoveGamesData(ZL):
    """ For efficiently storing openings stats for a particular move. """
    # Yes this is ugly, mapping different concepts to the same array.
    # BLACK wins: 0
    # WHITE wins: 1
    # total rt:   2
    # max rating: 3
    def __init__(self, initial_values=None):
        """ Using a persistent list wrapping around a python array.
            initial_values is for testing
        """
        if not initial_values:
            initial_values = [0,0,0,0]

        a = array.array('i', initial_values)
        ZL.__init__(self, a)

    def get_wins(self, colour):
        if colour == BLACK:
            return self[0]
        else:
            return self[1]

    def get_avg_rating(self):
        return int(float(self[2]) / (self[0] + self[1]))

    def get_max_rating(self):
        return self[3]

    def add_game(self, colour, rating):
        if colour == BLACK:
            self[0] += 1
        else:
            self[1] += 1
        self[2] += rating
        if self[3] < rating:
            self[3] = rating

class OpeningPosMoveData(ZM):
    """ Stores an OpeningMoveGamesData instance for each potential move,
    in a PersistentMapping (of a dict) """
    def __init__(self):
        ZM.__init__(self)

    def add_move(self, pos, *args):
        omd = self.setdefault(pos, OpeningMoveGamesData())
        omd.add_game(*args)

rules_map = {'s':0, 't':2, '5':4 }

def get_index(rules_type, size):
    """ Determine which slot of OpeningPos to use. """
    rt_char = rules_type[0]
    try:
        index = rules_map[rt_char]
    except KeyError:
        raise UnknownRuleType()
    if size == 19:
        index += 1
    else:
        if size != 13:
            raise UnknownSizeException("%s" % size)
    return index

class OpeningPos(ZL):
    """ All the stored information for a given opening position """
    def __init__(self):
        nothing_yet = [None] * 6
        ZL.__init__(self, nothing_yet)
        
    def add_move(self, rules_type, size, *args):
        ind = get_index(rules_type, size)
        omd = self[ind]
        if not omd:
            omd = self[ind] = OpeningPosMoveData()
        omd.add_move(*args)

    def get_moves_strict(self, rules_type, size):
        ind = get_index(rules_type, size)
        return self[ind]

    def __len__(self):
        tmp = [i for i in self if i]
        return len(tmp)

