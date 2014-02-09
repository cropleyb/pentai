import copy as c_m

class AIGenomeException(Exception):
    pass

class AIGenome(object):
    def __init__(self, name):
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
            "chokes": [(4,5)],
            "filter2": False,
            # Utility function
            "calc_mode": 1,
            "capture_score_base": 300,
            "take_score_base": 80,
            "threat_score_base": 20,
            "use_net_captures": True,
            "captures_scale": [1, 1, 1, 2, 4, 8],
            "length_scale": [1, 1, 1, 1, 1, 1],
            "length_factor": 35,
            "move_factor": 45,
            "vision": 100,
            "scale_pob": False,
            "force_depth": 0,
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
        return "Computer"

    def get_key(self):
        return self.p_key

    def __setattr__(self, attr_name, val):
        if hasattr(self, "override") and not self.override:
            if not hasattr(self, attr_name):
                raise AIGenomeException("Cannot set attribute %s" % attr_name)
        super(AIGenome, self).__setattr__(attr_name, val)

    def clone(self):
        c = c_m.copy(self)
        return c

