import help_screen as hs_m

class LoadHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Load/Edit Game Help"
        super(LoadHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
        TODO
"""
