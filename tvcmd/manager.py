from . import errors, cons, episode, show, config
from .sources import thetvdb, tvrage

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        
        self.episode_db = episode.DB()
        self.show_db = show.DB()
        
    def load(self):
        self.main.read()
        _source = self.main.get_source()
        
        if _source == "thetvdb": self.source = thetvdb.TheTVDB()
        elif _source == "tvrage": self.source = tvrage.TVRage()
        else: raise errors.ConfigError("Invalid source: %s" %(_source))
        
        self.status.read()
        
        self.episode_db.clear()
        self.show_db.clear()
            
    def save(self):
        # sync status
        for eurl in self.episode_db:
            if eurl["status"] == cons.NEW:
                self.status.remove(eurl.url())
            else:
                self.status.set(eurl.url(), eurl["status"])
        # write status
        self.status.write()
        
    def search_shows(self, pattern):
        shows = self.source.get_shows(pattern)
        db = show.DB()
        
        for s in shows:
            surl = show.Url(id=s["id"], name=s["name"])
            db.append(surl)
        
        return db
        
    def search_episodes(self, surl):
        episodes = self.source.get_episodes(surl["id"])
        db = episode.DB()
        
        for e in episodes:
            eurl = episode.Url(show=surl.url(), season=e["season"], episode=e["episode"], name=e["name"], date=e["date"])
            eurl.update(status = self.status.get(eurl.url()) or cons.NEW)
            db.append(eurl)
        
        return db
        
    def track(self, show_name):
        surl = self.search_shows(show_name)[0]
        edb = self.search_episodes(surl)
        self.show_db.append(surl)
        self.episode_db.extend(edb)
        
        return surl, edb
