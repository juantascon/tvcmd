import xdg.BaseDirectory, os

# episodes status
NEW = 0
ADQUIRED = 1
SEEN = 2
FUTURE = 3
    
ENUM_EPISODE_STATUS = {
    NEW: {"text": "NEW", "color": "" },
    ADQUIRED: {"text": "ADQUIRED", "color": "\033[33m" },
    SEEN: {"text": "SEEN", "color": "\033[32m" },
    FUTURE: {"text": "FUTURE", "color": "\033[34m" }
}

# config
CONFIGDIRBASE = "tvcmd"

# on debug config dir = ~/.config/tvcmd_debug/
if os.environ.get("DEBUG"):
    CONFIGDIRBASE += "_debug"

CONFIGDIR = xdg.BaseDirectory.save_config_path(CONFIGDIRBASE)
MAINCONFIGFILE = CONFIGDIR + "/main.cfg"
STATUSDBFILE = CONFIGDIR + "/status.db"
CACHEFILE = CONFIGDIR + "/cache.db"

# cache
CACHEDIR = xdg.BaseDirectory.save_cache_path("tvcmd")
