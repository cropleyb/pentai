import help_screen as hs_m

class SettingsHelpScreen(hs_m.HelpScreen):

    def __init__(self, *args, **kwargs):
        self.heading = "Settings Help"
        super(SettingsHelpScreen, self).__init__(*args, **kwargs)

    def set_text(self):
        sc = self.ids.scrollable_id
        sc.text1 = """
The Setting screen allows you to change how you want PentAI to behave, for all future interaction.

[b]User Interface[/b]

[i]Mark Moves[/i]
 The last two moves can be marked with a dot in the centre to make it easier to see what has happened recently.

[i]Show Captures[/i]
 When pieces were captured last move, the removed pieces are shown as transparent ghost pieces, just for one turn. You can still move there."""
        sc.text2 = """
[i]Move Confirmation[/i]
 If you find that you often slip when putting a piece on the board, you can turn on one of the move confirmation modes.
     [i]Off Board[/i] is safer - when you get it in the right place, click anywhere below the board to confirm the move. Use
     [i]None Required[/i] if you have good coordination and are in a stable location.
 Note that when you are placing a piece, you can slide your finger around to get it in the right place before letting go, and if you missed you can use the [i]Take Back[/i] button if required.

[i]Minimum Wait Time[/i]
 If you find it disconcerting for the AI to play instantly, you can set the smallest time that AI players will take to make a move.

[i]Show Confirmation Popups[/i]
 Would you prefer to confirm major actions before making them?"""
        sc.text3 = """
[b]Players[/b]

[i]Rematch first player[/i]
 When you choose [i]Rematch[/i] in the game screen, who should go first in the next game? You decide who will go first, out of:
- [i]Don't Swap[/i]
- [i]Alternate[/i]
- [i]Loser First[/i]

[i]First player colour[/i]
 Which colour should go first? If you have trouble remembering whether you are white or black, choose [i]Keep The Same[/i]
- [i]Always White[/i]
- [i]Always Black[/i]
- [i]Keep The Same[/i]"""
        sc.text4 = """
[b]Openings Book[/b]

[i]Add games[/i]
 Should completed games be added to the openings book?

[i]Build[/i]
 The openings book takes a while to build, and takes a fair amount of space.
 Expert players will want it be built in its entirity. Beginners will not notice a difference.
- [i]Don't Build[/i]: Just uses the experience of games played through your app.
- [i]Part On Startup[/i]: Takes a few seconds each time you start the app.
- [i]Build All Now[/i]: This takes a long time, but it only needs to be done once.
"""
        sc.text5 = """
[b]Sound[/b]

[i]Effects Volume[/i]
 You can adjust how loud the sound effects are.

[i]Tick[/i]
 If you play timed game a lot, the ticking noise can get annoying.

[i]Play win/loss sounds[/i]
 Similarly, the winning and losing sounds can get annoying.

[i]Music Volume[/i]
 You can adjust how loud the music is, or turn it off it you like. Turning it down to 0 then up again changes the track.
"""
