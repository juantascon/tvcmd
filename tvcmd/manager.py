from tvcmd import cons, episode, show, config, thetvdb
from tvcmd.errors import (ServerError, ConfigError, TrackError, SearchError)

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        
        self.episode_db = episode.DB()
        self.show_db = show.DB()
    
    def load(self):
        try: 
            self.status.read()
            self.main.read()
            
            self.episode_db.clear()
            self.show_db.clear()
        except Exception as ex:
            raise ConfigError("Error loading db (%s)"%(ex))
            
    def save(self):
        try:
            # sync status
            for eurl in self.episode_db:
                if eurl["status"] == cons.NONE:
                    self.status.remove(eurl.url())
                else:
                    self.status.set(eurl.url(), eurl["status"])
                    
            # write status
            self.status.write()
        except Exception as ex:
            raise ConfigError("Error saving db (%s)"%(ex))
        
    def search_shows(self, patternx):
        try:
            shows = thetvdb.get_shows(patternx)
            db = show.DB()
            
            for s in shows:
                surl = show.Url(id=s["id"], name=s["name"], language=s["language"])
                db.append(surl)
            
            return db
        except Exception as ex:
            raise SearchError("Error searching show %s (%s)"%(pattern, ex))
    
    def search_episodes(self, surl):
        try:
            episodes = thetvdb.get_episodes(surl["id"])
            db = episode.DB()
            
            for e in episodes:
                eurl = episode.Url(show=surl.url(), season=e["season"], episode=e["episode"], name=e["name"], date=e["date"])
                eurl.update(status = self.status.get(eurl.url()) or cons.NONE)
                db.append(eurl)
            
            return db
        
        except Exception as ex:
            raise SearchError("Error searching episodes %s (%s)"%(surl, ex))
        
    def track(self, show_name):
        try:
            surl = self.search_shows(show_name)[0]
            edb = self.search_episodes(surl)
            self.show_db.append(surl)
            self.episode_db.extend(edb)
        except Exception as ex:
            raise TrackError("Error tracking show %s (%s)"%(show_name, ex))
        
        return surl, edb
