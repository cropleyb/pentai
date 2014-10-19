from kivy.config import Config
from kivy.config import ConfigParser

import pentai.base.logger as log

import os

def config_instance():
    return _config

def create_config_instance(ini_file, user_path):
    global _config

    ini_path = os.path.join(user_path, ini_file)
    if not ini_file in os.listdir(user_path):
        log.info("Writing initial ini file %s" % ini_path)
        import shutil
        shutil.copy(ini_file, ini_path)
    else:
        log.info("Loading ini file from %s" % ini_path)

    _config = ConfigParser()
    _config.read(ini_path)

    log.info("Updating ini file from %s" % ini_file)
    _config.update_config(ini_file)
    # Don't need to write it back until something is changed.

    return _config
