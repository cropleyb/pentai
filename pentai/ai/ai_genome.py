import copy as c_m
from persistent import Persistent
from persistent.list import PersistentList as ZL
from persistent.mapping import PersistentMapping as ZM

class AIGenomeException(Exception):
    pass

class AIGenome(Persistent):
    def __init__(self, name, *args, **kwargs):
        super(AIGenome, self).__init__(*args, **kwargs)
        self.p_name = name
        self._saved_name = None
        self.p_key = None
        self.use_openings_book = True
        # Search params
        self.max_depth = 6
        self.max_depth_boost = 0
        self.mmpdl = 9
        self.narrowing = 0
        self.chokes = ((4,5),)
        self.bl_cutoff = False
        self.vision = 100

        # TODO: Remove, no longer used?
        self.utility_filter = False
        self.filter_num = 1

        # Utility function
        self.calc_mode = 1
        self.capture_score_base = 300
        self.take_score_base = 80
        self.threat_score_base = 20
        self.enclosed_four_base = 400
        self.use_net_captures = True
        self.captures_scale = (1, 1, 1, 2, 4, 8)
        self.length_scale = (1, 1, 1, 1, 1, 1)
        self.length_factor = 35
        self.move_factor = 45
        self.scale_pob = False
        self.force_depth = 0
        self.judgement = 100
        self.checkerboard_value = 35

        # dead
        self.length_boosts = () #ZL([]), # length, boost
        self.sub_type_boosts = () #ZL([]), # length, sub_type, boost):

    def get_name(self):
        try:
            name = self.p_name
        except AttributeError:
            name = self.name
            self.p_name = name
            del self.name
        return name

    def get_type(self):
        return "AI"

    def get_key(self):
        return self.p_key

    '''
    def __reduce__(self):
        print "IN REDUCE ---------------------------"
        return (self.__class__, (self.__dict__,))

    def _richcmp(self, other, compare_type):
        print "IN RICHCMP ---------------------------"
        v1 = self.p_key
        v2 = other.p_key
        if compare_type == 2:
            return v1 == v2
        elif compare_type == 3:
            return v1 != v2
        elif compare_type == 0:
            return v1 < v2
        elif compare_type == 1:
            return v1 <= v2
        elif compare_type == 4:
            return v1 > v2
        elif compare_type == 5:
            return v1 >= v2

    def __richcmp__(self, other, compare_type):
        return self._richcmp(other, compare_type)
    '''
