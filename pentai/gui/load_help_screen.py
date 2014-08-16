import help_screen as hs_m

class LoadHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Load/Edit Games Help"
        super(LoadHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
 Each game is summarised in two rows, listing the game number, the first and second players, the date the game was started, the rules variation used, and the size of the board.

[b]Load[/b]
 [i]In Progress[/i] games can be loaded, to be continued or reviewed. 
 Select the game, then click on [i]Load[/i] or double click. The list can be scrolled through.
 [i]Recently Finished[/i] games can also be loaded, for reviewing. Only the most recent games are shown.

[b]Edit[/b]
 Games can be adjusted after they are started, mainly to change the players or rules variation: Select the game, then click on [i]Edit[/i].

[b]Delete[/b]
 If the screen is filling up with old games, you can delete them: Select the game, then click on [i]Delete[/i]. There is no going back.
"""
