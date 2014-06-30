from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

import webbrowser

from scrollable_label import *
import pentai.base.logger as log

class MenuScreen(Screen):
    """ This is more of a travel agency or a directory than a menu """
    version_str = StringProperty("")
    about_text1 = StringProperty("")
    about_text2 = StringProperty("")
    about_text3 = StringProperty("")
    about_text4 = StringProperty("")
    about_text5 = StringProperty("")
    about_text6 = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)

        self.version_str = "0.9.1"

        self.ids.gl_id.ids.label1_id.bind(on_ref_press=self.follow_link)
        self.ids.gl_id.ids.label2_id.bind(on_ref_press=self.follow_link)
        self.about_text1 = \
"""      Pente is a strategy board game for two or more players, created in 1977 by Gary Gabrel. It is now owned by Hasbro, and the board game could be bought from [ref=ww][color=00ffff]Winning Moves[/color][/ref] until recently.

      Beginners: Watch the 2:30 "Rules Demo" and watch it to the end without touching the screen (it skips sections if you touch the screen). Create a new human player for youself, then start a game. Play your first game as the first player against "Anthony". Try to get five in a row. Then progress through the computer opponents alphabetically until you start to lose games. Don't skip too many or you may get disheartened!
"""
        self.about_text2 = \
"""      The rules of the game are very simple: The first player to get 5 stones in a straight line wins. Pairs of stones can be captured by placing a stone at each end of the pair. Capturing 5 pairs first also wins. Click "Rules Demo" below!

      PentAI is a computer program to play Pente. It can be configured to play in a wide range of ability levels, from a complete beginner to a strong amateur player. For more information about how PentAI works, see my [ref=bc][color=00ffff]website[/color][/ref].
"""
        self.about_text3 = \
"""      If you get a sore brain, you can create a game between a couple of Artificial Intelligence (AI) players and watch what they do. Human versus Human games are also possible, though you may prefer to play with a real set.

      Games are automatically saved, and can be resumed if they were left unfinished.
"""
        self.about_text4 = \
"""      There are a few settings that you might like to change, for things such as move confirmation style, sound volume and so on.

      Thanks go to:
"""
        self.about_text5 = \
"""- Alan Morris for the wonderful voiceover
- Marion and Noel Lodge for their constant support and feedback
- Thad Spreg for his expert Pente insights
- Mark Mammel for helpful discussions about implementing Pente strategy
- Annette Campbell for inspiring me to write this in the first place
- Sascha, Jespah and Arwen for their comments on "The Sod"
- The Kivy team for lots of help with their excellent toolset
- Liam Routt for games development advice
- Lots of other people for their support and feedback"""
        self.about_text6 = \
"""
Enjoy,
Bruce
"""
    def follow_link(self, inst, ref):
        log.debug("User clicked on: %s" % ref)
        if ref == "ww":
            link = "http://winning-moves.com"
        elif ref == "bc":
            link = "http://www.bruce-cropley.com/pentai"
        webbrowser.open_new_tab(link)

