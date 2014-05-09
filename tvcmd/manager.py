from . import errors, cons, episode, show, fs
from .sources import thetvdb, tvrage

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self._main = fs.Main()
        self._status = fs.Status()
        self._cache = fs.Cache()
        
        self.episodes = episode.List()
        self.shows = show.List()
        
        # has episodes status been modified?
        self.modified = False
        self.source = None
        self.formats = []
    
    def load(self):
        self.episodes.clear()
        self.shows.clear()
        
        # read every config file
        self._main.read()
        self._status.read()
        self._cache.read()
        
        # load formats
        self.formats = self._main.get_formats()
        
        # load source
        _source = self._main.get_source()
        if _source == "thetvdb": self.source = thetvdb.TheTVDB()
        elif _source == "tvrage": self.source = tvrage.TVRage()
        
        # load tracked shows
        for show_name in self._main.get_shows():
            s = show.Item(show_name)
            self.shows.append(s)
        
        # load episodes cache
        for k,v in self._cache.items():
            item = episode.Item.new_from_dict(v)
            
            # get only cache for tracked shows
            if len(self.shows.filter(lambda e: e.name == item.show)) == 0: continue
            
            # status defaults to NEW
            item.status = cons.NEW
            
            # load status from separate config file
            item_status = self._status.get(item.url())
            if item_status is not None:
                item.status = item_status
            
            self.episodes.append(item)
        
        self.modified = False
    
    def save_cache(self):
        for e in self.episodes:
            self._cache[e.url()] = e.to_dict()
        
        self._cache.write()
    
    def save_status(self):
        for e in self.episodes:
            self._status.set(e.url(), e.status)
        
        self._status.write()
        
        self.modified = False
    
    def search_episodes(self, show):
        raw_episodes = self.source.get_episodes(show.id)
        l = episode.List()
        
        for raw in raw_episodes:
            # includes show name in raw output for new_from_dict
            raw["show"] = show.url()
            e = episode.Item.new_from_dict(raw)
            
            #loads previous status
            e.status = self._status.get(e.url()) or cons.NEW
            l.append(e)
        
        return l
    
    def search_shows(self, pattern):
        raw_shows = self.source.get_shows(pattern)
        l = show.List()
        
        for raw in raw_shows:
            s = show.Item(raw["name"], raw["id"])
            l.append(s)
        
        return l
    
    def track(self, show_name):
        for s in self.search_shows(show_name):
            if s.url() == show_name:
                l = self.search_episodes(s)
                
                self.shows.upsert(s)
                self.episodes.upsert_r(l)
                
                return l
        
        raise errors.TrackError("Show not found, try: search")

# singleton
instance = Manager()
instance.load()
