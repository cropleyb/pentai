from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from scrollable_label import *
import pentai.base.logger as log
from pentai.gui.fonts import AI_FONT

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

        self.version_str = "0.9.2"

        self.intro_text = \
""" Pente is a strategy board game for two or more players, created in 1977 by Gary Gabrel. It is now owned by Hasbro, and the board game could be bought from [ref=ww][color=00ffff]Winning Moves[/color][/ref] until recently.
                  (scroll for more)"""
        self.beginners_text = \
"""1. First, edit [ref=hp][color=00ffff]Human Players[/color][/ref] to create a new human player for yourself.
2. Next, watch the 2.5min [ref=rd][color=00ffff]Rules Demo[/color][/ref] (button below) to the end, without touching the screen - it skips the current section if you touch the screen.
3. Start a [ref=ng][color=00ffff]New Game[/color][/ref]. Play your first game as the first player against
 [font=%s]Anthony[/font]. Try to get five in a row.
4. Continue through the computer opponents alphabetically until you start to lose games. Don't skip too many or you may get disheartened!""" % AI_FONT
        self.experts_text = \
"""1. Edit [ref=hp][color=00ffff]Human Players[/color][/ref] to create a new human player for yourself.
2. Then start a [ref=ng][color=00ffff]New Game[/color][/ref]. Play your first game as the first player against [font=%s]*killer*[/font].
3. If [font=%s]*killer*[/font] is too hard, try going through the alphabetically ordered AI players, starting with [font=%s]Henrietta[/font], or create an [ref=aip][color=00ffff]AI Player[/color][/ref] to your taste.
4. If [font=%s]*killer*[/font] is too easy for you, try [font=%s]Samuel[/font], or play timed games to make it tougher.
""" % (AI_FONT, AI_FONT, AI_FONT, AI_FONT, AI_FONT)
        self.about_text1 = \
""" PentAI is a computer program to play Pente. It can be configured to play in a wide range of ability levels, from a complete beginner to a strong amateur player. For more information about how PentAI works, see my [ref=bc][color=00ffff]website[/color][/ref].

 If you get a sore brain, you can create a game between a couple of
 [font=%s]Artificial Intelligence[/font] ([font=%s]AI[/font]) players and watch how they play. Human versus Human games can also be played with PentAI, though you may prefer to play with a real board.
""" % (AI_FONT, AI_FONT)
        self.about_text2 = \
""" Games are automatically saved, and can be resumed if they were left unfinished - see [ref=ip][color=00ffff]In Progress[/color][/ref].
 [ref=rf][color=00ffff]Recently Finished[/color][/ref] games can be reviewed.

There are a few [ref=settings][color=00ffff]Settings[/color][/ref] that you might like to change, for things such as move confirmation style, sound volume and so on.
"""
        self.ack_text = \
"""- Alan Morris for the wonderful voiceover
- Marion and Noel Lodge for their constant support and feedback
- Thad Spreg, Sven Chmiel (Lupulo) and del, for their expert Pente insights
- Mark Mammel for helpful discussions about implementing Pente strategy
- Annette Campbell for inspiring me to write this in the first place
- Sascha, Jespah and Arwen for their comments on "The Sod"
- Tara for lots of insights into the user interface
- The Kivy team for lots of help with their excellent toolset
- Liam Routt for games development advice
- Lots of other people for their support and feedback

 Enjoy,
 Bruce
"""

