
class MRUCache():
    def __init__(self, size):
        self.cache = []
        self.size = size

    def add(self, val):
        try:
            self.cache.remove(val)
        except ValueError:
            pass
        self.cache.append(val)
        
        if len(self.cache) > self.size:
            self.cache = self.cache[-self.size:]

    def top(self, num):
        ret = self.cache[-num:]
        ret.reverse()
        return ret
