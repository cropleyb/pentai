
# 1. Unzip openings games into data directory (if not there)
# 2. Add a number of games to the openings book db

import os
import parse_game as par_m
import pentai.base.pente_exceptions as pe_m
import zodb_dict as z_m
import openings_book as ob_m
import games_mgr as gm_m
import misc_db as m_m

def misc():
    return m_m.get_instance()

def unzip_openings(openings_dir):
    import zipfile as zf_m
    zip_path = "openings.zip"
    zf = zf_m.ZipFile(zip_path)
    target_directory = openings_dir
    os.makedirs(target_directory)
    zf.extractall(target_directory)

def add_games(openings_book, section_dir, start, count=100):

    game_files = os.listdir(section_dir)

    added = 0
    
    for gf in game_files[start:]:
        gf_path = os.path.join(section_dir, gf)
        gf_str = open(gf_path).readlines()
        try:
            g = par_m.convert_game(gf_str, int(gf))
        except pe_m.IllegalMoveException, e:
            print "%s: %s" % (gf, e.message)
        except pe_m.ParseException, e:
            print "%s: %s" % (gf, e.message)
        except Exception, e:
            print "%s: %s" % (gf, e.message)
        print "Adding: %s" % g.game_id
        try:
            #import pdb
            #pdb.set_trace()
            openings_book.add_game(g, update_cache=False, sync=False)
        except pe_m.OpeningsBookDuplicateException:
            pass

        added += 1
        if added >= count:
            break
    z_m.sync()
    return count - added

def build(openings_book, user_data_dir, section=None, start=None, count=100):
    # Extend library
    openings_dir = os.path.join(user_data_dir, "openings")
    if not os.path.isdir(openings_dir):
        unzip_openings(openings_dir)

    if not section:
        try:
            section = misc()["opening_section"]
        except:
            section = misc()["opening_section"] = 60

    if not start:
        try:
            start = misc()["opening_start"]
        except:
            start = misc()["opening_start"] = 0

    # TODO Stop adding games

    par_m.create_ai_players()

    remaining = count
    while remaining:
        section_dir = os.path.join(openings_dir, str(section))

        try:
            remaining = add_games(openings_book, section_dir, start, count)
        except OSError:
            pass

        if remaining:
            # Not enough games in that section
            start = 0
            section -= 1
            count = remaining
            if section < 30:
                break
        else:
            start += count

    misc()["opening_section"] = section
    misc()["opening_start"] = start
    z_m.sync()

def main():
    # TODO Move this to zodb_dict
    db_path = os.path.join(".", "db.fs")
    print "Loading DB from %s" % db_path
    lockfile_path = db_path + ".lock"
    if os.path.isfile(lockfile_path):
        os.unlink(lockfile_path)
        print "Cleared DB lock"

    z_m.set_db(db_path)

    import sys

    section = sys.argv[1]
    start = sys.argv[2]

    # HACK HACK HACK
    user_data_dir = "/Users/cropleyb/Library/Application Support/pentai"

    par_m.create_ai_players()

    games_mgr = gm_m.GamesMgr()
    openings_book = ob_m.OpeningsBook(games_mgr)

    build(openings_book, user_data_dir, section, start, 100)

if __name__ == "__main__":
    main()

