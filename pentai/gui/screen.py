import kivy.uix.screenmanager

class Screen(kivy.uix.screenmanager.Screen):

    def set_app(self, val):
        self.app = val

    def set_config(self, val):
        self.config = val

    def set_games_mgr(self, val):
        self.gm = val

    def set_openings_book(self, val):
        self.ob = val

    def set_players_mgr(self, val):
        self.pm = val

