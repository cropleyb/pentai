
# 1. Unzip openings games into data directory (if not there)
# 2. Add a number of games to the openings book db

import os
import parse_game as par_m
import pentai.base.pente_exceptions as pe_m
import zodb_dict as z_m
#import game_manager as gm_m

def unzip_openings(openings_dir):
    import zipfile as zf_m
    zip_path = "openings.zip"
    zf = zf_m.ZipFile(zip_path)
    target_directory = openings_dir
    os.makedirs(target_directory)
    zf.extractall(target_directory)

def add_games(openings_book, section_dir, start):
    game_files = os.listdir(section_dir)
    
    #import pdb
    #pdb.set_trace()
    for gf in game_files[start:start+10]:
        gf_path = os.path.join(section_dir, gf)
        gf_str = open(gf_path).readlines()
        #gf_lines = gf_str.split('\n')
        try:
            g = par_m.convert_game(gf_str, int(gf))
        except pe_m.IllegalMoveException, e:
            print "%s: %s" % (gf, e.message)
        except pe_m.ParseException, e:
            print "%s: %s" % (gf, e.message)
        except Exception, e:
            print "%s: %s" % (gf, e.message)
        print "Adding: %s" % g.game_id
        openings_book.games_mgr.save(g)
        #openings_book.add_game(g)
    z_m.sync()

def build(openings_book, user_data_dir):
    #import pdb
    #pdb.set_trace()
    openings_dir = os.path.join(user_data_dir, "openings")
    if not os.path.isdir(openings_dir):
        unzip_openings(openings_dir)

    section_dir = os.path.join(openings_dir, "38")

    par_m.create_ai_players()

    add_games(openings_book, section_dir, 0)

