import copy as c_m
from persistent import Persistent

class AIGenomeException(Exception):
    pass

class AIGenome(Persistent):
    def __init__(self, name, *args, **kwargs):
        super(AIGenome, self).__init__(*args, **kwargs)
        defaults = {
            "override": False,
            "p_name": name,
            "p_key": None,
            "use_openings_book": True,
            # Search params
            "max_depth": 6,
            "max_depth_boost": 0,
            "mmpdl": 9,
            "narrowing": 0,
            "chokes": ((4,5),),
            "bl_cutoff": False,
            "utility_filter": False,
            #"filter2": False,
            "filter_num": 1,
            "vision": 100,
            # Utility function
            "calc_mode": 1,
            "capture_score_base": 300,
            "take_score_base": 80,
            "threat_score_base": 20,
            "enclosed_four_base": 400,
            "use_net_captures": True,
            "captures_scale": (1, 1, 1, 2, 4, 8),
            "length_scale": (1, 1, 1, 1, 1, 1),
            "length_factor": 35,
            "move_factor": 45,
            "scale_pob": False,
            "force_depth": 0,
            "judgement": 100,
            "length_boosts": [], # length, boost
            "sub_type_boosts": [], # length, sub_type, boost):
        }
        super(AIGenome, self).__setattr__("__dict__", defaults)

    def set_override(self, val):
        self.override = val

    def get_name(self):
        try:
            name = self.p_name
        except AttributeError:
            name = self.name
            self.set_override(True)
            self.p_name = name
            del self.name
            self.set_override(False)
        return name

    def get_type(self):
        return "AI"

    def get_key(self):
        return self.p_key

    def __setattr__(self, attr_name, val):
        if hasattr(self, "override") and not self.override:
            if not hasattr(self, attr_name):
                raise AIGenomeException("Cannot set attribute %s" % attr_name)
        super(AIGenome, self).__setattr__(attr_name, val)

    def clone(self):
        c = c_m.deepcopy(self)
        return c

