from pentai.gui.screen import Screen
from kivy.properties import StringProperty

from pentai.gui.scrollable_label import *
import pentai.base.logger as log
from pentai.gui.fonts import *

class MenuScreen(Screen):
    """ This is more of a travel agency or a directory than a menu """
    version_str = StringProperty("")
    intro_text = StringProperty("")
    beginners_text = StringProperty("")
    experts_text = StringProperty("")
    about_text1 = StringProperty("")
    about_text2= StringProperty("")
    ack_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)

        self.version_str = "0.9.7"

        self.intro_text = conv(
""" Pente is a strategy board game for two or more players, created in 1977 by Gary Gabrel. If you are new to this App, follow the Guide by clicking on the flashing green areas.




   [b]Scroll[/b] (drag) for more, or click [REF=link]links[/REF]




""")
#It is now owned by Hasbro, and the board game could be bought from [REF=ww]Winning Moves[/REF] until recently.
        self.beginners_text = conv(
"""1. First, watch the 2.5min [REF=rd]Rules Demo[/REF] (button below) to the end, without touching the screen - it skips the current section if you touch the screen.
2. Start a [REF=ng]New Game[/REF]. Your first game will be You as the first player against [AI]Anthony[/AI]. Try to get five in a row first.
3. Next, edit [REF=hp]Human Players[/REF] to create a new human player for yourself.
4. Continue through the computer opponents alphabetically until you start to lose games. Don't skip too many or you may get disheartened!
""")
        self.experts_text = conv(
"""1. Edit [REF=hp]Human Players[/REF] to create a new human player for yourself.
2. Then start a [REF=ng]New Game[/REF] Play your first game as the first player against [AI]*killer*[/AI].
3. If [AI]*killer*[/AI] is too hard, try going through the alphabetically ordered AI players, starting with [AI]Henrietta[/AI], or create an [REF=aip]AI Player[/REF] to your taste.
4. If [AI]*killer*[/AI] is too easy for you, try [AI]Samuel[/AI], or play timed games to make it tougher.
""")
        self.about_text1 = conv(
""" PentAI is a computer program to play Pente. It can be configured to play in a wide range of ability levels, from a complete beginner to a strong amateur player. For more information about how PentAI works, see my [REF=bc]website[/REF].

 If you get a sore brain, you can create a game between a couple of
 [AI]Artificial Intelligence[/AI] ([AI]AI[/AI]) players and watch how they play. Human versus Human games can also be played with PentAI, though you may prefer to play with a real board.""")
        self.about_text2 = conv(
""" Games are automatically saved, and can be resumed if they were left unfinished - see [REF=ip]In Progress[/REF].
 [REF=rf]Recently Finished[/REF] games can be reviewed.

There are a few [REF=settings]Settings[/REF] that you might like to change, for things such as move confirmation style, sound volume and so on.
""")
        self.ack_text = conv(
"""- Alan Morris for the wonderful voiceover
- Marion and Noel Lodge for their constant support and feedback
- Thad Spreg, Sven Chmiel (Lupulo) and del, for their expert Pente insights
- Mark Mammel for helpful discussions about implementing Pente strategy
- Annette Campbell for inspiring me to write this in the first place
- Sascha, Jespah and Arwen for their comments on "The Sod"
- Tara for lots of insights into the user interface
- Richard B for many helpful suggestions
- The Kivy team for lots of help with their excellent toolset
- Liam Routt for games development advice
- Lots of other people for their support and feedback

 Enjoy,
 Bruce
""")

    def on_enter(self, *args, **kwargs):
        log.debug("Expanding openings book")

        self.app.openings_book._get_instance()
