
import persistent_dict as pd_m
import os

from defines import *

class MiscDB(pd_m.PersistentDict):
    """ Persistent Globals that don't belong in settings """
    def __init__(self, prefix=None, *args, **kwargs):
        global the_instance
        the_instance = self
        if prefix is None:
            prefix = os.path.join("db","")
        filename = prefix + "misc.pkl"
        super(MiscDB, self).__init__(filename, 'c', format="pickle")

the_instance = None

def get_instance():
    if not the_instance:
        MiscDB()
    return the_instance

