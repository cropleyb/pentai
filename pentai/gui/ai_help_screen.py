from kivy.uix.screenmanager import Screen

from scrollable_label import *

class HelpScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(HelpScreen, self).__init__(*args, **kwargs)

class AIHelpScreen(HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "AI Player Help"
        super(AIHelpScreen, self).__init__(*args, **kwargs)

    def on_pre_enter(self):
        self.set_text()

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """      You can either edit an existing player by selecting their name, or create a new one (leave the top box with "Create One", and type in the name immediately below).

      There are several settings that can be adjusted for a given Artificial Intelligence (AI) player profile:

    [i]Depth[/i]: Controls how many turns the AI looks ahead for each move.
    [i]Vision[/i]: How often does the AI see the better move possibilities?
    [i]Openings book[/i]: Should the AI be able to refer to previous games?
    [i]Judgement[/i]: How well should the AI judge the value of positions?"""

        sc.text2 = """
      The Openings Book uses positions that have been played previously with PentAI, and by many skilled players on pente.org. Every time you play a game against an AI Player, the result is added to the Openings Book, along with the first 12 or so moves.

      When you have finished editing, click on the Save button.

      Several profiles are included, have a look at and experiment with their configurations, or create your own. The AI players starting with a capital letter increase in difficulty alphabetically. Note that the players in *asterisks* are special, and do not follow any pattern.

"""
