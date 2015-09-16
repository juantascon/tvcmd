import xdg.BaseDirectory as xdg_dir, os

# episodes status
NEW = 0
ADQUIRED = 1
SEEN = 2
FUTURE = 3
IGNORED = 4
    
ENUM_EPISODE_STATUS = {
    NEW: {"text": "NEW", "color": "" },
    ADQUIRED: {"text": "ADQUIRED", "color": "\033[33m" },
    SEEN: {"text": "SEEN", "color": "\033[32m" },
    FUTURE: {"text": "FUTURE", "color": "\033[34m" },
    IGNORED: {"text": "IGNORED", "color": "\033[94m" }
}

BASE = "tvcmd"
if os.environ.get("DEBUG"):
    BASE = "tvcmd_debug"

CONFIG = xdg_dir.save_config_path(BASE)
CONFIG_MAIN = CONFIG + "/main.cfg"
CONFIG_STATUS = CONFIG + "/status.db"

CACHE = xdg_dir.save_cache_path(BASE)
CACHE_HTTP = CACHE + "/http"
CACHE_EPISODES = CACHE + "/episodes.db"
