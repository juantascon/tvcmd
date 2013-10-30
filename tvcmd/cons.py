import os
import xdg.BaseDirectory

# episodes status
NEW = 0
ADQUIRED = 1
SEEN = 2
FUTURE = 3

# ENUM_EPISODE_STATUS = {
#     NEW: {"text": "NEW", "color":"\033[31m" },
#     ADQUIRED: {"text": "ADQUIRED", "color":"\033[33m" },
#     SEEN: {"text": "SEEN", "color":"\033[32m" },
#     FUTURE: {"text": "FUTURE", "color":"\033[30m" } }

ENUM_EPISODE_STATUS = {
    NEW: {"text": "NEW", "color":"\033[01;38;5;245m" },
    ADQUIRED: {"text": "ADQUIRED", "color":"\033[01;38;5;142m" },
    SEEN: {"text": "SEEN", "color":"\033[01;38;5;70m" },
    FUTURE: {"text": "FUTURE", "color":"\033[01;38;5;129m" } }

# config
CONFIGDIR = xdg.BaseDirectory.save_config_path("tvcmd")
MAINCONFIGFILE = CONFIGDIR + "/main.cfg"
STATUSDBFILE = CONFIGDIR + "/status.db"

# cache
CACHEDIR = xdg.BaseDirectory.save_cache_path("tvcmd")

# thetvdb.com
APIKEY = "FD9D34DB64F25A09"
