
# For infinity def only
from alpha_beta import *

def utility(black_lengths, white_lengths, captures):
    bl = black_lengths
    wl = white_lengths
    score = 0
    if bl[4] > 0:
        return infinity
    if wl[4] > 0:
        return -infinity
    # TODO: check rules, use captures

    for i in range(len(bl)):
        rev = 4 - i
        score += bl[rev]
        score -= wl[rev]
        score *= 100
    return score
