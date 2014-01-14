from persistent_dict import *

class BaseDB(object):
    def __init__(self, filename):
        self.objs = PersistentDict(filename, 'c', format='pickle')
        
    def add(self, o):
        self.objs[o.key()] = o
        self.objs.sync()

    def remove(self, key):
        try:
            del self.objs[key]
            self.objs.sync()
            return True
        except KeyError:
            return False

    def find(self, key):
        try:
            return self.objs[key]
        except KeyError:
            return None

