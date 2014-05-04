import rot_standardise as rs_m
import trans_standardise as t_m

def standardise(orig_state): # Test code only
    possibilities = rs_m.rot_possibilities(orig_state)
    all_combined = []
    for p in possibilities:
        c = combine_and_trim(p)
        all_combined.append((c[0], c))

    try:
        s = min(all_combined)[1]
    except IndexError:
        import pdb
        pdb.set_trace()
    return s

def combine_and_trim(poss):
    rot_std, fwd, rev = poss

    both_std, lshift, dshift = t_m.shift(rot_std)
    trimmed = both_std.get_board().d_strips[0].strips
    while len(trimmed) and trimmed[-1] == 0:
        trimmed.pop()
    trimmed_tuple = tuple(trimmed)
    # Now combine lshift and dshift into fwd and rev
    def both_fwd(*pos):
        x, y = fwd(*pos)
        x -= lshift
        y -= dshift
        return x, y
    def both_rev(*pos):
        x, y = pos
        x += lshift
        y += dshift
        new_p = rev(x, y)
        return new_p
    return trimmed_tuple, both_fwd, both_rev

