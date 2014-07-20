
LENGTHS = 5
SUB_TYPES = 3

class LengthFactor(object):
    def __init__(self):
        self.default_factor = 2
        self.length_boosts = [1] * LENGTHS
        self.sub_type_boosts = [1] * (LENGTHS * SUB_TYPES)
        self.calc_weights()
    
    def set_default_factor(self, f):
        self.default_factor = f
        self.calc_weights()

    def set_length_boost(self, length, boost):
        self.length_boosts[length-1] = boost
        self.calc_weights()

    def set_sub_type_boost(self, length, sub_type, boost):
        ind = (length-1) * SUB_TYPES + sub_type
        self.sub_type_boosts[ind] = boost
        self.calc_weights()

    def calc_weights(self):
        max_ind = LENGTHS * SUB_TYPES
        self.weights = [0] * max_ind
        w = 1
        for i in range(max_ind):
            self.weights[i] = w
            if i % SUB_TYPES == (SUB_TYPES-1):
                l = i / SUB_TYPES
                try:
                    lb = self.length_boosts[l+1]
                    w *= lb
                except IndexError:
                    pass
                w *= self.default_factor
        for i, b in enumerate(self.sub_type_boosts):
            self.weights[i] *= b

    def get_weight(self, length, sub_type):
        ind = (length-1) * SUB_TYPES + sub_type
        return self.weights[ind]

    def get_weights(self):
        return self.weights
