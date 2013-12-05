# TODO: This will need to be increased to 6 for pente-keryo
COUNT_LENGTH=5

class LengthCounter():
    def __init__(self, arr=None):
        if arr == None:
            self.counts = [0] * COUNT_LENGTH
        else:
            self.counts = arr[:]

    def tup(self):
        return tuple(self.counts)

    def __eq__(self, other):
        return self.counts == other

    def __repr__(self):
        return str(self.counts)

    def __len__(self):
        return COUNT_LENGTH

    def __getitem__(self, i):
        return self.counts[i]


from defines import *
from candidate_accumulator import *

"""
Detect and report indices that build on or interfere with a 
possibly fragmented line, as well as counting these possibilities
"""

FIVE_OCCS_MASK = (4 ** 5 - 1)

global length_lookup

import pdb

def extend_and_store_lookups(occ, depth, occ_val, length, colour, rep_str):
    if occ != EMPTY:
        # add occ to lookup value
        occ_val += colour

        # add one to length
        length += 1
        rep_str = rep_str + str(colour)
    else:
        rep_str = rep_str + " "
    # TODO: if occ is EMPTY, save it for ca later

    if depth <= 1:
        if length > 0:
            # add_pattern
            assert length <= 5
            rep_str = rep_str + ">"
            length_lookup[occ_val] = colour, length, rep_str
    else:
        build_and_store_values(depth-1, occ_val, length, colour, rep_str)


def build_and_store_values(depth, occ_val, length, colour, rep_str=None):
    if rep_str == None:
        rep_str = "<"
    occ_val *= 4
    for occ in (EMPTY, colour):
        extend_and_store_lookups(occ, depth, occ_val, length, colour, rep_str)


def prepare_length_lookups():
    global length_lookup
    length_lookup = {}

    build_and_store_values(5, 0, 0, BLACK)
    build_and_store_values(5, 0, 0, WHITE)

prepare_length_lookups()

def process_substrips(bs, min_ind, max_ind, ca, black_counter, white_counter, inc):
    length_counters = [None, black_counter, white_counter]
    for ind in range(min_ind, 1+max_ind-4):
        shift = ind << 1 # x 2 for 2 bits each occ
        occs = (bs.occs >> shift) & FIVE_OCCS_MASK
        try:
            colour, length, rep_str = length_lookup[occs]
        except:
            continue
        lc = length_counters[colour]
        lc.counts[length-1] += inc
        # TODO: ca

