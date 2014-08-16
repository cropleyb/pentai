import help_screen as hs_m

class HumanHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Human Player Help"
        super(HumanHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
 You can either edit an existing player by selecting their name, or create a new one. Leave the top box with
 [i]Create One[/i], and type in your name in the white area immediately below, where it says [i]Give me a Name[/i].

 At the moment, the only thing you can change about a human player is their name.
"""
