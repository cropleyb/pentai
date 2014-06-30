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
    #if True:
        log.info("Copying ini")
        import shutil
        shutil.copy(ini_file, ini_path)

    _config = ConfigParser()
    _config.read(ini_path)

    return _config
