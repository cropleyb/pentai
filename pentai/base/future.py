
import importlib

class Future(object):
    def __init__(self, cls_name, mod_name, *args, **kwargs):
        self._cls_name = cls_name
        self._mod_name = mod_name
        self._args = args
        self._kwargs = kwargs
        self._instance = None

    def _get_instance(self):
        if not self._instance:
            #import pdb
            #pdb.set_trace()
            mod = importlib.import_module(self._mod_name)
            cls = getattr(mod, self._cls_name)
            self.__dict__["_instance"] = cls(*self._args, **self._kwargs)
        return self._instance

    def __getattr__(self, attr_name):
        inst = self._get_instance()
        return getattr(inst, attr_name)

    '''
    # This would be nice, but it interferes with __getattr__ and gets into an
    # infinite loop. TODO
    def __setattr__(self, attr_name, val):
        inst = self._get_instance()
        return setattr(inst, attr_name, val)
    '''

