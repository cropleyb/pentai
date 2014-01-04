from defines import *

import random

import pdb

class BlindnessFilter():
    def __init__(self, wrapped_filter):
        self.wrapped_filter = wrapped_filter
        self.blindness = 0

    def __getattr__(self, field_name):
        return getattr(self.wrapped_filter, field_name)

    def set_blindness(self, blindness):
        self.blindness = blindness

    def copy(self, *args, **kwargs):
        new_inner = self.wrapped_filter.copy(*args, **kwargs)
        new_bf = BlindnessFilter(new_inner)
        new_bf.blindness = self.blindness
        return new_bf

    def get_iter(self, *args, **kwargs):
        passed = 0
        for m in self.wrapped_filter.get_iter(*args, **kwargs):
            rand_val = random.random()
            if rand_val > self.blindness:
                yield m
                passed += 1
        if passed == 0:
            yield m
