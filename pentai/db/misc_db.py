
import zodb_dict as zd_m
import os

the_instance = None

def get_instance(prefix=None):
    global the_instance
    if the_instance is None:
        the_instance = zd_m.get_section("misc")
    return the_instance

def reset():
    global the_instance
    the_instance = None

