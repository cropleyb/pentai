import help_screen as hs_m

from pentai.gui.fonts import *
from kivy.properties import StringProperty

class HumanHelpText(hs_m.HelpText):
    edit_text = StringProperty("")

    def __init__(self, *args, **kwargs):
        self.title = "Human Player Editor Help"
        self.set_text()
        super(HumanHelpText, self).__init__(*args, **kwargs)

    def set_text(self):
        self.edit_text = """ You can edit an existing player by selecting their name, or create a new one. Leave the top box with
 [i]Create One[/i], and type in your name in the white area immediately below, where it says [i]Give me a Name[/i]. If you feel like it, you can even delete a human player. This will have no effect in the real world.

 At the moment, the only thing you can change about a human player is their name.

 Saving is automatic.
"""

class HumanHelpScreen(hs_m.NewHelpScreen):
    help_text_class = HumanHelpText

