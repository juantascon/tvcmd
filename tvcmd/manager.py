from . import errors, cons, episode, show, config
from .sources import thetvdb, tvrage

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        self.episodes = episode.List()
        self.shows = show.List()
        
    def load(self):
        self.main.read()
        _source = self.main.get_source()
        if _source == "thetvdb": self.source = thetvdb.TheTVDB()
        elif _source == "tvrage": self.source = tvrage.TVRage()
        
        self.status.read()
        self.episodes.clear()
        self.shows.clear()
        
    def save(self):
        # sync status
        for e in self.episodes:
            if e.status == cons.NEW:
                self.status.remove(e.url())
            else:
                self.status.set(e.url(), e.status)
        # write status
        self.status.write()
        
    def search_episodes(self, show):
        raw_episodes = self.source.get_episodes(show.id)
        l = episode.List()
        
        for raw in raw_episodes:
            e = episode.Item(show.url(), raw["season"], raw["episode"], raw["name"], raw["date"])
            e.status = self.status.get(e.url()) or cons.NEW
            l.append(e)
        
        return l
    
    def search_shows(self, pattern):
        raw_shows = self.source.get_shows(pattern)
        l = show.List()
        
        for raw in raw_shows:
            s = show.Item(raw["id"], raw["name"])
            l.append(s)
        
        return l
    
    def track(self, show_name):
        s = self.search_shows(show_name)[0]
        l = self.search_episodes(s)
        self.shows.append(s)
        self.episodes.extend(l)
        
        return l
