from pentai.base import rules, game, human_player
import pentai.db.games_mgr as gm_m

def create_game(game_str):
    bs = 13
    rstr = 's'
    r = rules.Rules(bs, rstr)

    player1 = human_player.HumanPlayer("Black")
    player2 = human_player.HumanPlayer("White")

    g = game.Game(r, player1, player2) # To be replaced shortly
    remainder = g.configure_from_str(game_str)
    g.load_moves(remainder)
    return g

def create_game_from_filename(filename):
    f = open(filename)
    s = f.read()
    g = create_game(s)
    gm = gm_m.GamesMgr()
    gm.save(g)

create_game_from_filename("games/Kang_Professor_2014-03-28.txt")

