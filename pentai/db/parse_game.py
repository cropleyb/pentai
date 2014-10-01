
import pentai.base.game as g_m
import pentai.base.rules as r_m
import pentai.base.human_player as h_m
import players_mgr as pm_m
from pentai.base.defines import *
from pentai.base.pente_exceptions import *
import pentai.ai.ai_genome as aig_m


g_s = """
[Game "Pente"]
[Site "Pente.org"]
[Event "Turn-based Game"]
[Round "-"]
[Section "-"]
[Date "01/19/2014"]
[Time "21:22:25"]
[TimeControl "5"]
[Rated "Y"]
[Player 1 Name "xtraclassy"]
[Player 2 Name "data22"]
[Player 1 Rating "2488"]
[Player 2 Rating "1696"]
[Player 1 Type "Human"]
[Player 2 Type "Human"]
[Result "1-0"]

1. K10 M9 2. N10 M7 3. M8 O7 4. L10 J10 5. M10 O10 6. L9 N7 7. L7 P7 8. Q7 L11
9. L8 L6 10. K8 J9 11. J11 H12 12. J8 N8 13. H8 1-0
"""

import pdb

def parse_game(game_str):
    if type(game_str) is list:
        lines = game_str
    else:
        lines = game_str.split('\n')


    metadata = {}
    moves = ""
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == '[':
            section, val = line[1:-1].split('\"', 1)
            section = section[:-1]
            val = val[:-1]
            metadata[section] = val[:-2]
        else:
            moves = moves + ' ' + line

    move_list = moves.split(' ')
    result = move_list.pop()

    ml2 = []
    for m in move_list:
        m = m.strip()
        if not len(m):
            continue
        if m[-1] == '.':
            continue
        x_c = m[0]
        x = ord(x_c) - ord('A')
        if x >= 9:
            x -= 1
        y = int(m[1:]) - 1
        ml2.append((x, y),)

    return metadata, ml2, result

def convert_game(game_str, key):
    metadata, moves, result = parse_game(game_str)

    g = g_m.Game()
    r = r_m.Rules(19, 's')

    p1 = h_m.HumanPlayer(metadata["Player 1 Name"])
    p2 = h_m.HumanPlayer(metadata["Player 2 Name"])
    p1.set_rating(int(metadata["Player 1 Rating"]))
    p2.set_rating(int(metadata["Player 2 Rating"]))
    g.setup(rules=r, player1=p1, player2=p2)

    for m in moves:
        g.make_move(m)
    won_by = g.get_won_by()
    g.game_id = key
    if not won_by:
        recorded_result = metadata["Result"]
        if recorded_result[0] == "1":
            g.set_won_by(P1)
        if recorded_result[0] == "0":
            g.set_won_by(P2)

    return g

