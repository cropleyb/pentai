import help_screen as hs_m

class HumanHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Human Player Help"
        super(HumanHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
You can either edit an existing player by selecting their name, or create a new one (leave the top box with "Create One", and type in the name immediately below).

At the moment there is nothing else to change about a human player besides their name.
Make sure you [TODO FONT] Save before leaving.
"""
