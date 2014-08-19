import help_screen as hs_m

from pentai.gui.fonts import AI_FONT
from kivy.properties import StringProperty

class LoadHelpText(hs_m.HelpText):
    intro_text = StringProperty("")
    load_text = StringProperty("")
    edit_text = StringProperty("")
    delete_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.heading = "Load/Edit Games Help"
        self.set_text()
        super(LoadHelpText, self).__init__(*args, **kwargs)

    def set_text(self):
        self.intro_text = """ Each game is summarised in two rows, listing the game number, the first and second players, the date the game was started, the rules variation used, and the size of the board.
"""
        self.load_text = """ [i]In Progress[/i] games can be loaded, to be continued or reviewed. 
 Select the game, then click on [i]Load[/i] or double click. The list can be scrolled through.
 [i]Recently Finished[/i] games can also be loaded, for reviewing. Only the most recent games are shown.
"""
        self.edit_text = """ Games can be adjusted after they are started, mainly to change the players or rules variation: Select the game, then click on [i]Edit[/i].
"""
        self.delete_text = """ If the screen is filling up with old games, you can delete them: Select the game, then click on [i]Delete[/i]. There is no going back.
"""

class LoadHelpScreen(hs_m.NewHelpScreen):
    help_text_class = LoadHelpText

