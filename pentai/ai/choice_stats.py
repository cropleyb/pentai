
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
        self.all_vals = [[] for d in range(MAX_DEPTH)]
        self.max_move_ind_seen = 0
        self.max_depth_seen = 0
        self.totals = [0 for d in range(MAX_DEPTH)]
        self.bl_filtered_ok = [0 for d in range(MAX_DEPTH)]
        self.bl_filtered_bad = [0 for d in range(MAX_DEPTH)]

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
        #self.save_rel_vals(depth, save_values)
        self.save_best_last_filtered(depth, save_values)
        self.save_all_vals(depth, save_values)

    def save_best_ind(self, depth, save_values):
        best_val = 0
        best_ind = 0
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

    # Need to save all values 
    def save_all_vals(self, depth, save_values):
        self.all_vals[depth].append(save_values[:])

    def save_best_last_filtered(self, depth, save_values):
        triggered = False
        for i, val in enumerate(save_values):
            self.totals[depth] += 1
            if not triggered:
                if i == 0:
                    best_val = val
                    worst_val = val
                else:
                    if val > best_val:
                        best_val = val
                    elif val < worst_val:
                        worst_val = val
                        triggered = True
            else:
                if val < best_val:
                    self.bl_filtered_ok[depth] += 1
                else:
                    self.bl_filtered_bad[depth] += 1

    def filtered_ok_relative_to_best_n_worst(self, depth):
        try:
            return float(self.bl_filtered_ok[depth]) / self.totals[depth]
        except ZeroDivisionError:
            return 0

    def filtered_bad_relative_to_best_n_worst(self, depth):
        try:
            return float(self.bl_filtered_bad[depth]) / self.totals[depth]
        except ZeroDivisionError:
            return 0

    def set_threshold(self, val):
        self.threshold = val

    # Can this be done after the games have been played?
    # Need to keep all the move scores, in order, per position/turn

    def filtered_thresh(self, depth):
        # How many were filtered ok relative to the threshold?
        t = self.threshold
        av_d = self.all_vals[depth]
        ok = 0
        bad = 0
        total = 0
        for t, av_t in enumerate(av_d):
            triggered = False
            for i, val in enumerate(av_t):
                if not triggered:
                    if i == 0 or val > chosen_best:
                        chosen_best = val
                    else:
                        if EXP_BASE ** (val - chosen_best) < self.threshold:
                            triggered = True
                else:
                    if val < chosen_best:
                        ok += 1
                    elif val > chosen_best:
                        bad += 1
            total += len(av_t)
        try:
            total = float(total)
            return ok/total, bad/total
        except ZeroDivisionError:
            return 0,0

    '''
    def filtered_bad_thresh(self, depth):
        # How many were filtered out incorrectly relative to the threshold?
        # i.e. better than the chosen best value
        # TODO
        pass
    '''

    def filtered_ok_relative_to_best_n_worst(self, depth):
        try:
            return float(self.bl_filtered_ok[depth]) / self.totals[depth]
        except ZeroDivisionError:
            return 0

    def filtered_bad_relative_to_best_n_worst(self, depth):
        try:
            return float(self.bl_filtered_bad[depth]) / self.totals[depth]
        except ZeroDivisionError:
            return 0
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

        lines.append("")
        for d in range(self.max_depth_seen + 1):
            l = "Depth %s B/L Skipped %s OK, missed %s" % (d,
                self.filtered_ok_relative_to_best_n_worst(d),
                self.filtered_bad_relative_to_best_n_worst(d))
            lines.append(l)

        return "\n".join(lines)

    def f_t_disp(self):
        lines = []
        for d in range(self.max_depth_seen + 1):
            ok, bad = self.filtered_thresh(d)
            l = "Depth %s FT OK %s, BAD %s" % (d, ok, bad)
            lines.append(l)

        return "\n".join(lines)
