import logging
def log(): return logging.getLogger(__name__)

def fmt_url(show, season, episode):
    torrentz = "https://torrentz.eu/verified?f=%s+s%02de%02d" % (show.replace("_", "+"), season, episode)
    log().debug("torrentz: %s"%(torrentz))
    
    ezrss = "http://ezrss.it/search/index.php?show_name=%s&season=%d&episode=%d&mode=advanced" % (show.replace("_", "+"), season, episode)
    log().debug("ezrss: %s"%(ezrss))
    
    btjunkie = "https://btjunkie.org/search?q=%s+s%02de%02d" % (show.replace("_", "+"), season, episode)
    
    return "\n".join([torrentz, ezrss, btjunkie])
