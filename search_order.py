
class PosIterator:
    """ Iterate over all the positions on the board. Central positions are visited first.
    """
    def __init__(self, board_size):
        sqr_list = []
        centre_coord = board_size / 2
        for x in range(board_size):
            for y in range(board_size):
                p = (x, y)
                dist_sqr_from_centre = (x - centre_coord) ** 2 + (y - centre_coord) ** 2
                sqr_list.append((dist_sqr_from_centre, p))

        sqr_list.sort()
        self.pos_list = [i[1] for i in sqr_list]

    def get_iter(self):
        for p in self.pos_list:
            yield p

