# TODO: This will need to be increased to 6 for pente-keryo
COUNT_LENGTH=5

from defines import *
from candidate_accumulator import *

"""
Detect and report indices that build on or interfere with a 
possibly fragmented line, as well as counting these possibilities.
Here, we build a lookup table, which is a mapping from a bit pattern
to the information we need - the colour, current length and empty indices
of the row of 5 positions that we are currently looking at.
"""

FIVE_OCCS_MASK = (4 ** 5 - 1)

global length_lookup
length_lookup = {}

def extend_and_store_lookups(occ, depth, occ_val, length, colour, empty_list, rep_str):
    """
    occ is the colour of the stone (or EMPTY) that we are extending by
    depth is the length yet to be added
    occ_val is the total value so far, representing the stretch to the left
    that we have already processed.
    length is the number of stones seen so far in that stretch. They will all
    have been of the same 'colour' as we only care about and store them if
    they are.
    rep_str is a representation of the stones seen so far, for debugging.
    """
    if occ != EMPTY:
        # add occ to lookup value
        occ_val += colour

        # add one to length
        length += 1
        rep_str = rep_str + str(colour)
    else:
        rep_str = rep_str + " "
        empty_list.append(depth)

    if depth <= 0:
        if length > 0:
            # add_pattern
            assert length <= 5
            rep_str = rep_str + ">"
            length_lookup[occ_val] = colour, length, sorted(empty_list), rep_str
    else:
        # Recursively add to the stretch
        build_and_store_values(depth-1, occ_val, length, colour, empty_list[:], rep_str)


def build_and_store_values(depth, occ_val, length, colour, empty_list, rep_str=None):
    """ Add one stone or empty place """
    # For debugging.
    if rep_str == None:
        rep_str = "<"

    # Shift what we've seen so far to the right
    occ_val *= 4
    for occ in (EMPTY, colour):
        extend_and_store_lookups(occ, depth, occ_val, length, colour, empty_list[:], rep_str)


def prepare_length_lookups():
    """ Build the entire lookup table """
    # We only care about stretches of 5 with one colour and empties in it.
    build_and_store_values(4, 0, 0, BLACK, [])
    build_and_store_values(4, 0, 0, WHITE, [])

# TODO: Something better than a global
prepare_length_lookups()

def process_substrips(bs, min_ind, max_ind, ca, length_counters, inc):
    """
    Try to match each stretch of 5 positions against our lookup table.
    If we find a match then report the number of stones of the same
    colour via length_counters, and report the empty locations (indices)
    for use by the search filter (ca = CandidateAccumulator)
    If we are removing the contributions, inc will be set to -1
    """

    for ind in range(min_ind, 1+max_ind-4):
        # Extract just the 5 * 2 bits that we're currently interested in.
        shift = ind << 1 # x 2 for 2 bits each occ - EMPTY:0, BLACK:1 or WHITE:2
        occs = (bs.occs >> shift) & FIVE_OCCS_MASK

        # Now see if it's in our lookup table
        try:
            colour, length, empty_list, rep_str = length_lookup[occs]
        except KeyError:
            # Nope. Not interesting.
            continue

        # Found a match
        lc = length_counters[colour]
        # Count it
        lc[length-1] += inc

        # Report it
        shifted_empties = [e+ind for e in empty_list]
        ca.report_length_candidate(colour, length, shifted_empties)

