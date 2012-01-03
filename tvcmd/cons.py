import os

# episodes status
NEW = 0
ADQUIRED = 1
SEEN = 2
ENUM_EPISODE_STATUS = { NEW: "NEW", ADQUIRED: "ADQUIRED", SEEN: "SEEN" }

# config
CONFIGDIR = os.environ["XDG_CONFIG_HOME"]+"/tvcmd"
MAINCONFIGFILE = "main.cfg"
STATUSDBFILE = "status.cfg"

# cache
CACHEDIR = os.environ["XDG_CACHE_HOME"]+"/tvcmd"

# thetvdb.com
APIKEY = "FD9D34DB64F25A09"
