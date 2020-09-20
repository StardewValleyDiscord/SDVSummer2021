import json, os

dir_path = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(dir_path, "../private/database.db")

_config_path = os.path.join(dir_path, "../private/config.json")
with open(_config_path) as config_file:
    cfg = json.load(config_file)

DISCORD_KEY = cfg['discord']
CMD_PREFIX = cfg['command_prefix']
TEAMS = cfg['teams']
SIGNUP_MES = cfg['channels']['signup']
