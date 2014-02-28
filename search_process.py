
from players_mgr import PlayersMgr
from defines import *
from kivy.clock import Clock
from preserved_game import *

from multiprocessing import *

class SearchProcess(object):

    def search(self, preserved_game):
        pm = PlayersMgr()
        game = preserved_game.restore(pm, update_cache=False)
        game.resume()
        p = game.get_current_player()
        m = p.do_the_search()
        return m

    def search_and_respond(self, conn, preserved_game):
        move = self.search(preserved_game)
        conn.send(move)
        conn.close()

    def create_process(self, game, gui):
        pg = PreservedGame(game)
        self.gui = gui
        self.parent_conn, child_conn = Pipe()
        self.process = Process(target=self.search_and_respond,
                args=(child_conn, pg,))
        self.process.start()
        Clock.schedule_interval(self.poll, .05)

    def poll(self, ignored):
        ready = self.parent_conn.poll()
        if ready:
            Clock.unschedule(self.poll)
            self.receive()

    def receive(self):
        answer = self.parent_conn.recv()
        self.process.join() # TODO: Reuse the process.
        self.gui.enqueue_action(answer)

    def kill(self):
        self.process.kill()
