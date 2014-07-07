
import string

from pentai.base.defines import *

# Overkill
MAX_MOVE_NUM = 30
MAX_DEPTH = 30

EXP_BASE = 1.01

class ChoiceStats(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.best_vals_at = [([0.0] * MAX_MOVE_NUM) for d in range(MAX_DEPTH)]
        self.rel_val_to_best_val = [[] for d in range(MAX_DEPTH)]
        self.max_move_ind_seen = 0
        self.max_depth_seen = 0

    def report_vals(self, depth, save_values):
        if len(save_values) > self.max_move_ind_seen:
            self.max_move_ind_seen = len(save_values)
        if depth > self.max_depth_seen:
            self.max_depth_seen = depth

        if depth % 2:
            try:
                save_values = [-sv for sv in save_values]
            except:
                #st()
                pass

        best_ind, best_val = self.save_best_ind(depth, save_values)
        self.save_rel_val(depth, save_values, best_ind, best_val)

    def save_best_ind(self, depth, save_values):
        for i, val in enumerate(save_values):
            if i == 0:
                best_val = val
                best_ind = i
            else:
                if val > best_val:
                    best_val = val
                    best_ind = i

        self.best_vals_at[depth][best_ind] += 1
        return best_ind, best_val

    def save_rel_val(self, depth, save_values, best_ind, best_val):

        if best_ind == 0:
            return
        min_val_before_best = min(save_values[:best_ind])

        try:
            #rv = (EXP_BASE ** min_val_before_best) / (EXP_BASE ** best_val)
            rv = EXP_BASE ** (min_val_before_best - best_val)
        
            self.rel_val_to_best_val[depth].append(rv)
        except ZeroDivisionError:
            #st()
            pass

    def get_best_vals_at(self, depth):
        return self.best_vals_at[depth][:self.max_move_ind_seen]

    def rel_val_list(self, depth):
        return self.rel_val_to_best_val[depth]

    def safe_threshold(self, depth, best):
        return 1.0
        
    def __repr__(self):
        lines = ["Best value was at:"]
        cols = ["\tv%s" % d for d in range(self.max_move_ind_seen)]
        title = ["Depth "]
        title.extend(cols)
        #st()
        line = string.join(title, "")
        #lines.append("".join(title))
        lines.append(line)
        for d, vals in enumerate(self.best_vals_at[:self.max_depth_seen+1]):
            vals[self.max_move_ind_seen:] = []
            l = "%s%s" % (d, "".join(["\t%d" % v for v in vals]))
            lines.append(l)
        return "\n".join(lines)

'''
Depth v1  v2  v3  v4  v5  v6  v7  v8  v9
  1   40  30  20   5   5
'''
