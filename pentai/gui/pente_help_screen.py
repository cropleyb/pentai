import help_screen as hs_m
import pentai.base.logger as log

from pentai.gui.fonts import *
from kivy.properties import StringProperty

class PenteHelpText(hs_m.HelpText):
    play_text1 = StringProperty("")
    play_text2 = StringProperty("")
    play_text3 = StringProperty("")
    controls_text1 = StringProperty("")
    controls_text2 = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.title = "Pente Game Screen Help"
        self.set_text()
        super(PenteHelpText, self).__init__(*args, **kwargs)

    def set_text(self):
        self.play_text1 = """ To make a move, simply touch the board where you want to go. If you have "Off Board" confirmation mode on, you will need to confirm the move once you get the piece in the right place. To do this, simply touch anywhere in the green area below the board.

 If you need a refresher on the rules, watch the [ref=rd][color=00ffffff]Rules Demo[/color][/ref]"""

        self.play_text2 = """ The places where pieces were captured show a faint "ghost" image just for the opponent's next turn. You can play over these ghosts. If you are playing Standard or Tournament rules, the pieces that were captured appear in pairs below the board, and when one player reaches five pairs, they win.

 Last move markers are shown with a dot in the middle of the pieces that were placed in the last two turns."""

        self.play_text3 = """ If you make a mistake, you can [i]Take Back[/i] if no-one is watching over your shoulder! If you are playing against an AI player, you will want to get the game back to a point where it was your turn, so you may need to click [i]Take Back[/i] twice.

 Most of these features can be configured on the [ref=settings][color=00ffffff]Settings[/color][/ref] screen.
"""
        self.controls_text1 = """ There are two modes: [i]Play[/i] mode and [i]Review[/i] mode:
 - In [i]Play[/i] mode, the two players alternate whose turn it is to place a piece on the board, until the game is finished.
 - In [i]Review[/i] mode, you can go
 [i]Forward[/i] and [i]Backward[/i] through the move history of the game.
 
 The screen switches to [i]Review[/i] mode automatically at the end of a game. To switch to [i]Play[/i] mode, use the
 [i]Continue[/i] button."""

        self.controls_text2 = """ You can quickly start another game with the same rules and players, by using "Rematch". Who goes first in the next game, and the colours of the players, are determined by the
 [ref=settings][color=00ffffff]Settings[/color][/ref].
"""

class PenteHelpScreen(hs_m.NewHelpScreen):
    help_text_class = PenteHelpText

