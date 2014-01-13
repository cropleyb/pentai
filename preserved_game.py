from persistent_dict import *

class PreservedGame():
    def game_name(self):
        return "Freddo" # TODO

class AllPreservedGames():
    def __init__(self, filename):
        self.games = PersistentDict(filename, 'c', format='pickle')

    def add_game(self, pg):
        self.games[pg.game_name()] = pg
        self.games.sync()
'''
# TODO
    with PersistentDict('/tmp/demo.json', 'c', format='json') as d:
        print(d, 'start')
        d['abc'] = '123'
        d['rand'] = random.randrange(10000)
        print(d, 'updated')

    # Show what the file looks like on disk
    with open('/tmp/demo.json', 'rb') as f:
        print(f.read())
'''
