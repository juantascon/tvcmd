import os

# for episodes
NONE = 0
ADQUIRED = 1
SEEN = 2

# for shows
TRACKED = 1
IGNORED = 2

# config
CONFIGDIR = os.environ["XDG_CONFIG_HOME"]+"/tvcmd"
MAINCONFIGFILE = "main.cfg"
STATUSDBFILE = "status.cfg"

# cache
CACHEDIR = os.environ["XDG_CACHE_HOME"]+"/tvcmd"

# thetvdb.com
APIKEY = "FD9D34DB64F25A09"
