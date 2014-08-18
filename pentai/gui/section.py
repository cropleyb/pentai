from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
from kivy.properties import *
import webbrowser

from pentai.base.defines import *
import pentai.base.logger as log

class Section(GridLayout):
    title = StringProperty("")
    text = StringProperty("")
    continuation = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(Section, self).__init__(*args, **kwargs)

    def follow_link(self, inst, ref):
        log.debug("User clicked on: %s" % ref)

        p = self.parent
        app = None
        while not app:
            try:
                app = p.app
            except AttributeError:
                p = p.parent

        if ref == "ww":
            link = "http://winning-moves.com"
            webbrowser.open_new_tab(link)
        elif ref == "bc":
            link = "http://www.bruce-cropley.com/pentai"
            webbrowser.open_new_tab(link)
        elif ref == "hp":
            app.show_human_screen()
        elif ref == "aip":
            app.show_ai_screen()
        elif ref == "rd":
            app.show_demo()
        elif ref == "ng":
            app.show_new_game_screen()
        elif ref == "ip":
            app.show_games_screen(finished=False)
        elif ref == "rf":
            app.show_games_screen(finished=True)
        elif ref == "settings":
            app.show_settings_screen()
'''
    def __init__(self, *args, **kwargs):
        self.cols = 1

        super(GridLayout, self).__init__(*args, **kwargs)
'''

