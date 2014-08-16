import help_screen as hs_m
import pentai.base.logger as log

class PenteHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Pente Game Screen Help"
        super(PenteHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.ids.label1_id.bind(on_ref_press=self.follow_link)
        sc.ids.label3_id.bind(on_ref_press=self.follow_link)
        sc.text1 = """
[b]Game Play[/b]

 To make a move, simply touch the board where you want to go. If you have "Off Board" confirmation mode on, you will need to confirm the move once you get the piece in the right place. To do this, simply touch anywhere in the green area below the board.

 If you need a refresher on the rules, watch the [ref=rd][color=00ffff]Rules Demo[/color][/ref]"""
        sc.text2 = """
The places where pieces were captured show a faint "ghost" image just for the opponent's next turn. You can play over these ghosts. If you are playing Standard or Tournament rules, the pieces that were captured appear in pairs below the board, and when one player reaches five pairs, they win.

 Last move markers are shown with a dot in the middle of the pieces that were placed in the last two turns."""
        sc.text3 = """
 If you make a mistake, you can [i]Take Back[/i] if no-one is watching over your shoulder! If you are playing against an AI player, you will need to get the game back to a point where it was your turn.

 Most of these features can be configured on the [ref=settings][color=00ffff]Settings[/color][/ref] screen.

[b]Controls[/b]
 """
    def follow_link(self, inst, ref):
        log.debug("User clicked on: %s" % ref)
        if ref == "rd":
            self.app.show_demo()
        elif ref == "settings":
            self.app.show_settings_screen()
        # TODO: more links
