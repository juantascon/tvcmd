from . import errors, cons, episode, show, io
from .sources import thetvdb, tvrage

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.main = io.Main()
        self.status = io.Status()
        self.cache = io.Cache()
        
        self.episodes = episode.List()
        self.shows = show.List()
        
    def load(self):
        self.main.read()
        _source = self.main.get_source()
        if _source == "thetvdb": self.source = thetvdb.TheTVDB()
        elif _source == "tvrage": self.source = tvrage.TVRage()
        
        self.status.read()
        self.cache.read()
        
        self.episodes.clear()
        self.shows.clear()
        
        for k,v in self.cache.items():
            self.episodes.append(episode.Item.new_from_dict(v))
    
    def save_cache(self):
        for e in self.episodes:
            self.cache[e.url()] = e.to_dict()
        
        self.cache.write()
    
    def save_status(self):
        for e in self.episodes:
            # deletes NEWs and insert/update the rest
            if e.status == cons.NEW:
                self.status.remove(e.url())
            else:
                self.status.set(e.url(), e.status)
        
        self.status.write()
        
        
    def search_episodes(self, show):
        raw_episodes = self.source.get_episodes(show.id)
        l = episode.List()
        
        for raw in raw_episodes:
            # includes show name in raw output for new_from_dict
            raw["show"] = show.url()
            e = episode.Item.new_from_dict(raw)
            
            #loads previous status
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
        self.episodes.upsert_r(l)
        
        return l
