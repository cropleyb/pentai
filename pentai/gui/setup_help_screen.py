import help_screen as hs_m

from pentai.gui.fonts import AI_FONT
from kivy.properties import StringProperty

class SetupHelpText(hs_m.HelpText):
    rules_text = StringProperty("")
    clocks_text = StringProperty("")
    players_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.title = "Game Setup Help"
        self.set_text()
        super(SetupHelpText, self).__init__(*args, **kwargs)

    def set_text(self):
        self.rules_text = """ There are three variations of the rules that are supported by PentAI.
 All variants can be won by getting 5 or more of your pieces in a continuous, straight line first.
 [i]Standard[/i] and [i]Tournament[/i] games are always started in the centre, so that move is played automatically.

 [i]Standard games[/i] can also be won by capturing 5 pairs first.

 [i]Tournament[/i] games are the same as Standard rules, but the 2[sup]nd[/sup] move by the 1[sup]st[/sup] player cannot be within two intersections of the centre point.

 [i]5-In-A-Row[/i] games can only be won with 5 in a row. Captures are allowed, but they don't cause a win to be triggered.
"""
        self.clocks_text = """ If you want a bigger challenge, you can turn on the clocks. They give each player a number of minutes to complete the game. If you run out of time before the game is finished, you lose.
"""
        self.players_text = """ Select the types of the first (to move) and second players, from [i]Human[/i] or
 [i]Computer[/i]. Then select the particular player of that type from the list below.  
"""

class SetupHelpScreen(hs_m.NewHelpScreen):
    help_text_class = SetupHelpText
