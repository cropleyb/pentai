
class GenomeException(Exception):
    pass

class Genome(object):
    def __init__(self, name):
        defaults = {
            "name": name,
            "use_openings_book": True,
            # Search params
            "max_depth": 6,
            "max_depth_boost": 0,
            "mmpdl": 9,
            "narrowing": 0,
            "chokes": [(4,5)],
            "filter2": True,
            # Utility function
            "capture_score_base": 300,
            "take_score_base": 100,
            "threat_score_base": 20,
            "captures_scale": [0, 1, 1, 1, 1, 1],
            "length_factor": 27,
            "move_factor": 30,
            "blindness": 0,
            "sub": True,
        }
        super(Genome, self).__setattr__("__dict__", defaults)

    def __setattr__(self, attr_name, val):
        if not hasattr(self, attr_name):
            raise GenomeException("Cannot set attribute %s" % attr_name)
        super(Genome, self).__setattr__(attr_name, val)

    def key(self):
        return self.name
