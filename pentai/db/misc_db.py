
import persistent_dict as pd_m
import os

from pentai.base.defines import *

class MiscDB(pd_m.PersistentDict):
    """ Persistent Globals that don't belong in settings """
    def __init__(self, prefix=None, *args, **kwargs):
        global the_instance
        the_instance = self
        if prefix is None:
            prefix = os.path.join("db","")
        filename = get_filename(prefix)
        super(MiscDB, self).__init__(filename) #, 'c', format="pickle")

def get_filename(prefix):
    return prefix + "misc.pkl"

the_instance = None

def get_instance(prefix=None):
    if the_instance is None:
        MiscDB(prefix)
    return the_instance

def delete(prefix):
    global the_instance
    try:
        os.unlink(get_filename(prefix))
    except:
        pass
    the_instance = None
