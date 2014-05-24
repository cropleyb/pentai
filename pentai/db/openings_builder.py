
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

def unzip_section(section, user_data_dir):
    print "unzipping %s" % section
    import zipfile as zf_m
    zip_path = os.path.join("openings", "%s.zip" % section)
    try:
        zf = zf_m.ZipFile(zip_path)
    except IOError:
        return False
    target_directory = os.path.join(user_data_dir, "openings")
    try:
        os.makedirs(target_directory)
    except OSError:
        pass
    zf.extractall(target_directory)
    return True

def add_games(openings_book, section_dir, start, count=100):

    game_files = os.listdir(section_dir)

    added = 0

    for gf in game_files[start:]:
        gf_path = os.path.join(section_dir, gf)
        gf_str = open(gf_path).readlines()
        try:
            g = par_m.convert_game(gf_str, int(gf))
            add_game(openings_book, g)
            added += 1
            if added >= count:
                break
        except pe_m.IllegalMoveException, e:
            print "%s: %s" % (gf, e.message)
        except pe_m.ParseException, e:
            print "%s: %s" % (gf, e.message)
        except Exception, e:
            print "%s: %s" % (gf, e.message)
    z_m.sync()
    return count - added

def add_game(openings_book, g):
    print "Adding: %s" % g.game_id
    try:
        openings_book.add_game(g, update_cache=False, sync=False)
    except pe_m.OpeningsBookDuplicateException:
        pass

import pdb

def build(openings_book, user_data_dir, section=None, start=None, count=100):
    # TEMP
    #print misc()["recent_ai_player_ids"]
    #print misc()["recent_human_ids"]
    #pdb.set_trace()
    '''
    from pentai.db.mru_cache import *
    mca = MRUCache(30)
    mca.cache = [211, 212, 213, 214, 215, 216, 217, 220, 221, 223, 224, 226, 227, 228, 229, 225, 222, 219, 218, 210]
    misc()["recent_ai_player_ids"] = mca
    mch = MRUCache(30)
    mch.cache = [30574, 30575, 30576, 30577, 30579, 30580, 30581, 30582, 30584, 30585, 30586, 30587, 30589, 30590, 30591, 30592, 30594, 30595, 30596, 30597, 30599, 30600, 30601, 30602, 30604, 30605, 30606, 30607, 30617, 209]
    misc()["recent_human_ids"] = mch
    '''
    '''
    misc()["recent_ai_player_ids"] = None
    misc()["recent_human_ids"] = None
    del misc()["recent_ai_player_ids"]
    del misc()["recent_human_ids"]
    '''
    z_m.sync()

    # Extend library
    if not section:
        try:
            section = misc()["opening_section"]
        except:
            section = misc()["opening_section"] = 60

    openings_dir = os.path.join(user_data_dir, "openings")
    section_dir = os.path.join(openings_dir, str(section))

    if not os.path.isdir(section_dir):
        # That will be enough startup time for now.
        return unzip_section(section, user_data_dir)

    if not start:
        try:
            start = misc()["opening_start"]
        except:
            start = misc()["opening_start"] = 0

    par_m.create_ai_players()

    remaining = count
    while remaining:
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
    return True

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

