import help_screen as hs_m

class SetupHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Game Setup Help"
        super(SetupHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """[b]Rules[/b]
There are three variations of the rules that are supported by PentAI.
All variants can be won by getting 5 or more of your pieces in a continuous, straight line first. [i]Standard[/i] and [i]Tournament[/i] games are always started in the centre, so that move is played automatically.

[i]Standard games[/i] can also be won by capturing 5 pairs first.
"""

        sc.text2 = """ [i]Tournament[/i] games are the same as Standard rules, but the 2[sup]nd[/sup] move by the 1[sup]st[/sup] player cannot be within two intersections of the centre point.

[i]5-In-A-Row[/i] games can only be won with 5 in a row. Captures are allowed, but they don't cause a win to be triggered.
"""

        sc.text3 = """ [b]Clocks[/b]
If you want a bigger challenge, you can turn on the clocks. They give each player a number of minutes to complete the game. If you run out of time before the game is finished, you lose.

[b]Player selection[/b]
Select the types of the first (to move) and second players, from [i]Human[/i] or [i]Computer[/i]. Then select the particular player of that type from the list below.  
"""
