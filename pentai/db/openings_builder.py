
# 1. Unzip openings games into data directory (if not there)
# 2. Add a number of games to the openings book db

import os
import shutil
import parse_game as par_m
import pentai.base.pente_exceptions as pe_m
import pentai.db.zodb_dict as z_m
import pentai.db.openings_book as ob_m
import pentai.db.games_mgr as gm_m
from misc_db import misc

from pentai.base.defines import *
import pentai.base.logger as log

def unzip_section(section, user_data_dir):
    log.info("unzipping %s" % section)
    import zipfile as zf_m
    zip_path = os.path.join("openings", "%s.zip" % section)
    try:
        zf = zf_m.ZipFile(zip_path)
    except IOError:
        # HACK!
        misc()["opening_section"] -= 1
        return section == 48

    target_directory = os.path.join(user_data_dir, "openings")
    try:
        os.makedirs(target_directory)
    except OSError:
        log.warn("OSError creating %s" % target_directory)
        pass
    zf.extractall(target_directory)
    return True

def remove_unzipped(section, user_data_dir):
    target_directory = os.path.join(user_data_dir, "openings", "%s" % section)

    log.info("removing unzipped from %s" % target_directory)
    shutil.rmtree(target_directory, ignore_errors=True)
    

def add_games(openings_book, section_dir, start, count=100):

    game_files = os.listdir(section_dir)

    added = 0

    for gf in game_files[start:]:
        gf_path = os.path.join(section_dir, gf)
        gf_str = open(gf_path).readlines()
        try:
            g = par_m.convert_game(gf_str, int(gf))
            add_game(openings_book, g, g.get_won_by())
            global total_added
            total_added += 1
            added += 1
            if added >= count:
                break
        except Exception, e:
            log.debug("%s: %s" % (gf, e.message))
    z_m.sync()
    return count - added

def add_game(openings_book, g, won_by):
    log.info("Adding: %s" % g.game_id)
    try:
        openings_book.add_game(g, won_by)
    except pe_m.OpeningsBookDuplicateException:
        pass

def is_finished():
    try:
        return misc()["opening_section"] < 34
    except KeyError:
        return False

def build(openings_book, user_data_dir, section=None, start=None, count=100):
    # Extend library
    if not section:
        try:
            section = misc()["opening_section"]
        except:
            section = misc()["opening_section"] = 50

    openings_dir = os.path.join(user_data_dir, "openings")
    section_dir = os.path.join(openings_dir, str(section))
    
    if not os.path.isdir(section_dir):
        if not unzip_section(section, user_data_dir):
            return True
        else:
            return False
    
    if not start:
        try:
            start = misc()["opening_start"]
        except:
            start = misc()["opening_start"] = 0

    remaining = count
    while remaining:
        try:
            remaining = add_games(openings_book, section_dir, start, count)
        except OSError:
            pass

        if remaining:
            # Not enough games in that section
            # We've finished with the current section so get rid of the
            # unzipped games directory.
            remove_unzipped(section, user_data_dir)
            start = 0
            section -= 1
            count = remaining
            break
        else:
            start += count

    misc()["opening_section"] = section
    misc()["opening_start"] = start
    z_m.sync()
    log.debug("Completed: section: %s; start game: %s" % (section, start))
    return False

total_added = 0

if __name__ == "__main__":
    from main import setup_logging
    setup_logging()
    db_path = os.path.join(".", "db.fs")
    z_m.set_db(db_path)
    import pentai.db.openings_book as ob_m
    openings_book = ob_m.OpeningsBook()
    while True:
        if build(openings_book, ".", count=100):
            break
        section = misc()["opening_section"]
        log.debug("built %s games so far, in section %s" % (total_added, section))
    log.debug("Finished building %s games, now packing" % total_added)
    z_m.pack()
