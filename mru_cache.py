
class MRUCache():
    def __init__(self, size):
        self.cache = []
        self.size = size

    def add(self, val):
        self.delete(val)
        self.cache.append(val)
        
        if len(self.cache) > self.size:
            self.cache = self.cache[-self.size:]

    def delete(self, val):
        try:
            self.cache.remove(val)
        except ValueError:
            pass

    def top(self, num):
        ret = self.cache[-num:]
        ret.reverse()
        return ret
