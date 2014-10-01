from pentai.base.defines import *
from pentai.db.preserved_game import *
from pentai.db.players_mgr import PlayersMgr

from multiprocessing import *

class SearchProcess(object):
    def __init__(self, listener):
        self.listener = listener
        self.process = None

    def search(self, preserved_game):
        pm = PlayersMgr()
        game = preserved_game.restore(pm, update_cache=False)
        game.resume()
        p = game.get_current_player()
        a = p.do_the_search()
        return a

    def search_and_respond(self, conn, preserved_game):
        move = self.search(preserved_game)
        conn.send(move)
        conn.close()

    def create_process(self, game):
        pg = PreservedGame(game)
        self.parent_conn, child_conn = Pipe()
        self.process = Process(target=self.search_and_respond,
                args=(child_conn, pg,))
        self.process.start()
        self.poll()

    def poll(self, ignored=None):
        ready = self.parent_conn.poll()
        if ready:
            self.receive()
        else:
            from kivy.clock import Clock
            Clock.schedule_once(self.poll, .05)

    def receive(self):
        answer = self.parent_conn.recv()
        self.process.join() # TODO: Reuse the process.
        self.listener.enqueue_action(answer)

    def terminate(self):
        if self.process:
            self.process.terminate()
