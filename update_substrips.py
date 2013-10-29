
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
