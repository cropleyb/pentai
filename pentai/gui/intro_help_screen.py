import help_screen as hs_m

class IntroHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Openings Book Builder Help"
        super(IntroHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
What this screen is really doing is building the openings book. If you are a complete beginner, you probably want to just [i]Skip[/i] this and turn it off in the [i]Settings[/i] screen. It takes a while - e.g. OS X 8mins, iOS 
"""
