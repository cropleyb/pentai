DIRECTIONS = ((-1,-1),(-1,0),(-1,1),
               (0,-1),        (0,1),
               (1,-1), (1,0), (1,1))

class Pos():
    def __init__(self, x, y):
        self.tup = (x,y)

    def __getitem__(self, dim):
        return self.tup[dim]

    def shift(self, direction, steps):
        new_pos = (self.tup[0] + (direction[0] * steps), \
                   self.tup[1] + (direction[1] * steps)) 
        return Pos(*new_pos)

    def __eq__(self, other):
        return self.tup[0] == other[0] and \
               self.tup[1] == other[1]

    def __repr__(self):
        return str(self.tup)

    def off_board(self, size):
        return self.tup[0] < 0 or \
               self.tup[0] >= size or \
               self.tup[1] < 0 or \
               self.tup[1] >= size
