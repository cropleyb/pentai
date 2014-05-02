import rot_standardise as rs_m
import trans_standardise as t_m

def standardise(orig_state):
    rot_std, fwd, rev = rs_m.standardise(orig_state)
    both_std, lshift, dshift = t_m.shift(rot_std)
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
    return both_std, both_fwd, both_rev

