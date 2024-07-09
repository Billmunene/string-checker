import configparser

def load_config(config_file='server_config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

config = load_config()
