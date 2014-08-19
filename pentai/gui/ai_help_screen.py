import help_screen as hs_m

from pentai.gui.fonts import AI_FONT
from kivy.properties import StringProperty


class AIHelpText(hs_m.HelpText):
    intro_text = StringProperty("")
    properties_text = StringProperty("")
    openings_text = StringProperty("")
    profiles_text= StringProperty("")

    def __init__(self, *args, **kwargs):
        self.heading = "AI Player Help"
        self.set_text()
        super(AIHelpText, self).__init__(*args, **kwargs)

    def set_text(self):
        self.intro_text = """ You can either edit an existing player by selecting their name (choose under "Create One"), or create a new one (leave the top box with "Create One", and type in the name immediately below).
"""

        self.properties_text = """ There are several properties that can be adjusted for a given [font=%s]Artificial[/font] [font=%s]Intelligence[/font] (AI) player profile:

 [i]Depth[/i]: Controls how many turns the AI looks ahead for each move.
 [i]Vision[/i]: How often does the AI see the better move possibilities?
 [i]Openings book[/i]: Should the AI be able to refer to previous games?
 [i]Judgement[/i]: How well should the AI judge the value of positions?
 """ % (AI_FONT, AI_FONT)

        self.openings_text = """ The Openings Book uses positions that have been played previously with PentAI, and by many skilled players on pente.org. Every time you play a game against an AI Player, the result is added to the Openings Book, along with the first 12 or so moves. (unless you disable this in [i]Settings[/i])

 When you have finished creating or editing an AI Player, click on the Save button. TODO: Make it automatic like HumanScreen.
"""

        self.profiles_text = """ Several profiles are included. Have a look at, and experiment with their configurations, or create your own. The AI players starting with a capital letter increase in difficulty alphabetically. Note that the players in [font=%s]*asterisks*[/font] are special, and do not follow any pattern.

""" % (AI_FONT,)

class AIHelpScreen(hs_m.NewHelpScreen):
    help_text_class = AIHelpText

    #title_text = "AI Player Help"
