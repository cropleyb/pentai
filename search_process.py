
from games_mgr import GamesMgr
from defines import *
from kivy.clock import Clock

from multiprocessing import *

class SearchProcess(object):

    def search(self, gid): # TODO: Use preserved game
        gm = GamesMgr()
        game = gm.get_game(gid)
        game.resume()
        p = game.get_current_player()
        m = p.do_the_search()
        return m

    def search_and_respond(self, conn, gid):
        move = self.search(gid)
        conn.send(move)
        conn.close()

    def create_process(self, gid, gui):
        self.gui = gui
        self.parent_conn, child_conn = Pipe()
        self.process = Process(target=self.search_and_respond, args=(child_conn,gid,))
        self.process.start()
        Clock.schedule_interval(self.poll, .05)

    def poll(self, ignored):
        ready = self.parent_conn.poll()
        if ready:
            Clock.unschedule(self.poll)
            self.receive()

    def receive(self):
        answer = self.parent_conn.recv()
        print answer
        self.process.join() # TODO: Reuse the process.
        self.gui.enqueue_action(answer)
