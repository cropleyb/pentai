#!/usr/bin/python

class UtilityCalculator():
    def __init__(self):
        self.captured_score_base = 120 ** 3
        self.take_score_base = 350
        self.threat_score_base = 20
        self.captures_scale = [0, 2.0, 4.6, 10.0, 22.0, 46.0]

    """ Captures become increasingly important as we approach 5 """
    def captured_contrib(self, captures):
        # TODO: Use rules?
        contrib = captures * self.captured_score_base * \
                self.captures_scale[captures/2]
        return contrib

    def take_contrib(self, takes):
        """ TODO takes become increasingly important as we approach 5 captures """
        # TODO: Use rules?
        contrib = takes * self.take_score_base
        return contrib

    def threat_contrib(self, threats):
        """ TODO threats become increasingly important as we approach 5 captures """
        # TODO: Use rules?
        contrib = threats * self.threat_score_base
        return contrib

