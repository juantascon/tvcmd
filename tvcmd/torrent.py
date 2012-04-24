import logging
def log(): return logging.getLogger(__name__)

def fmt_url(show, season, episode):
    torrentz = "https://torrentz.eu/verified?f=%s+s%02de%02d" % (show.replace("_", "+"), season, episode)
    fenopy = "http://fenopy.eu/search/%s+s%02de%02d.html?quality=1" % (show.replace("_", "+"), season, episode)
    # ezrss = "http://ezrss.it/search/index.php?show_name=%s&season=%d&episode=%d&mode=advanced" % (show.replace("_", "+"), season, episode)
    # btjunkie = "https://btjunkie.org/search?q=%s+s%02de%02d" % (show.replace("_", "+"), season, episode)
    
    return "\n".join([torrentz, fenopy])
