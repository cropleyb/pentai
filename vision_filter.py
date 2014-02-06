from defines import *

import random

import pdb

class VisionFilter():
    def __init__(self, wrapped_filter):
        self.wrapped_filter = wrapped_filter
        self.vision = 0

    def __getattr__(self, field_name):
        return getattr(self.wrapped_filter, field_name)

    def set_vision(self, vision):
        self.vision = vision

    def copy(self, *args, **kwargs):
        new_inner = self.wrapped_filter.copy(*args, **kwargs)
        new_bf = VisionFilter(new_inner)
        new_bf.vision = self.vision
        return new_bf

    def get_iter(self, *args, **kwargs):
        passed = 0
        for m in self.wrapped_filter.get_iter(*args, **kwargs):
            rand_val = random.random()
            if rand_val < self.vision:
                yield m
                passed += 1
        if passed == 0:
            yield m
