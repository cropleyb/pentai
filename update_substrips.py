import pdb

class LengthCounter():
    def __init__(self):
        self.counts = [0,0,0,0,0]

    def tup(self):
        return tuple(self.counts)

    def add(self, length):
        self.counts[length-1] += 1


# TODO give this a better home
def add_substrips(pattern, us_counter, them_counter):
    # pdb.set_trace()
    seen = [0, 0]

    i = 0
    old = []
    for occ in pattern:
        if occ > 0:
            seen[occ-1] +=  1
        old.append(occ)
        i += 1
        if i >= 5:
            if seen[0] > 0 and seen[1] == 0:
                us_counter.add(seen[0])
            elif seen[1] > 0 and seen[0] == 0:
                them_counter.add(seen[1])
            old_occ = old[i-5]
            if old_occ > 0:
                seen[old_occ-1] -= 1
    


'''
def convert_to_hash_value_list(pattern):
    ret = []
    # (U)s, (T)hem, ( )empty or (#)off-board
    code = {
        ' ': 0,
        'U': 1,
        'T': 2,
    }
    if pattern[0] != '#':
        # patterns with an edge can not be transposed
        # these are the non-edge patterns
        for i in range (10 - len(pattern)):
            hash_val = 0
            for c in pattern:
                hash_val = hash_val * 3
                # Left shift in base 3 == multiply by 3
                # 000001 -> 000010 (1 -> 3)
                # 000002 -> 000020 (2 -> 6)
                # 000021 -> 000210 (7 -> 21)
                v = code[c]
                hash_val += v
            hash_val *= (3 ** i)
            # ret.append(hash_val)
            add_unknown_combination_vals(ret, hash_val, i, len(pattern), 9)

    return ret

import itertools

def add_unknown_combination_vals(ret, hash_val, i, pattern_length, max_pattern_length):
    params = [[3] for j in range(i)]
    prod = itertools.product(*params) # , [hash_val])

    for h in prod:
        print h
        ret.append(hash_val + h)
'''
