from tvcmd import cons, episode, show, config, thetvdb
from tvcmd.errors import (ServerError, ConfigError, TrackError)

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        
        self.episodes = episode.DB()
        self.shows = show.DB()
    
    def load(self):
        self.status.read()
        self.main.read()
        
        self.episodes.clear()
        self.shows.clear()
    
    def save(self):
        try:
            # sync status
            for eurl in self.episodes:
                if eurl["status"] == cons.NONE:
                    self.status.remove(eurl.url())
                else:
                    self.status.set(eurl.url(), eurl["status"])
                    
            # write status
            self.status.write()
        except Exception as ex: raise ConfigError("Error saving db (%s)"%(ex))
                    
    def search_shows(self, show_name):
        db = show.DB()
        try:
            for s in thetvdb.get_show_info(show_name):
                surl = show.Url(id=s["id"], name=s["name"], language=s["language"])
                db.append(surl)
        except ServerError as ex: raise ex
        
        return db
    
    def search_episodes(self, surl):
        db = episode.DB()
        
        try:
            episodes = thetvdb.get_episodes(surl.url(), surl["id"])
            
            for e in episodes:
                eurl = episode.Url(show=e["show"], season=e["season"], episode=e["episode"], name=e["name"], date=e["date"])
                eurl.update(status = self.status.get(eurl.url()) or cons.NONE)
                db.append(eurl)
        except Exception as ex:
            raise TrackError("Error tracking show %s: (%s)"%(surl, ex))
        
        return db
