
import zodb_dict as zd_m
import os

the_instance = None

def get_instance(prefix=None):
    global the_instance
    if the_instance is None:
        the_instance = zd_m.get_section("db/misc.pkl")
    return the_instance

