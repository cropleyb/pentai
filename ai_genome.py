
class AIGenomeException(Exception):
    pass

class AIGenome(object):
    def __init__(self, name):
        defaults = {
            "override": False,
            "name": name,
            "key": None,
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
            "use_net_captures": False,
            "captures_scale": [1, 1, 1, 2, 4, 8],
            "length_scale": [1, 1, 1, 1, 1, 1],
            "length_factor": 35,
            "move_factor": 45,
            "blindness": 0,
            "scale_pob": True,
            "force_depth": 0,
        }
        super(AIGenome, self).__setattr__("__dict__", defaults)

    def set_override(self, val):
        self.override = val

    def __setattr__(self, attr_name, val):
        if hasattr(self, "override") and not self.override:
            if not hasattr(self, attr_name):
                raise AIGenomeException("Cannot set attribute %s" % attr_name)
        super(AIGenome, self).__setattr__(attr_name, val)

