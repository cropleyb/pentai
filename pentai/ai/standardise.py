import rot_standardise as rs_m
import trans_standardise as t_m

def standardise(orig_state):
    rot_std, fwd, rev = rs_m.standardise(orig_state)
    both_std, lshift, dshift = t_m.shift(rot_std)
    # Now combine lshift and dshift into fwd and rev
    def both_fwd(pos):
        new_p = fwd(pos)
        new_p[0] -= lshift
        new_p[1] -= dshift
        return new_p
    def both_rev(pos):
        pos[0] += lshift
        pos[1] += dshift
        new_p = rev(pos)
        return new_p
    return both_std, both_fwd, both_rev

