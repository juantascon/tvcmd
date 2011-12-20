#! /usr/bin/env python

import thetvdb.api
import fnmatch

class Url():
    
    COLOR_PENDING = "\033[31m"
    COLOR_SEEN = "\033[32m"
    COLOR_FUTURE = "\033[33m"
    COLOR_END = "\033[0m"
    
    def __init__(self, show, season, episode):
        self.show = show
        self.season = season
        self.episode = episode
        
    def fmt(self):
        info = thetvdb.api.get_episode_info(self.show, self.season, self.episode)
        
        try: name = info["episodename"]
        except: name = "N/A"
        
        try: date = info["firstaired"]
        except: date = "N/A"
        
        return "%s : [ %s ] [ %s ]" % (str(self), date, name)
        
    def fmt_color(self, seen):
        return (self.COLOR_SEEN if seen else self.COLOR_PENDING) + self.fmt() + self.COLOR_END
    
    def fmt_episode(self):
        return ( "e%02d" %(self.episode) if self.episode != -1 else "")
    
    def fmt_season(self):
        return ( "s%02d" %(self.season) if self.season != -1 else "")
    
    def fmt_show(self):
        return self.show + "."
    
    def __repr__(self):
        return self.fmt_show() + self.fmt_season() + self.fmt_episode()
    
    @classmethod
    def parse(cls, _str):
        parts1 = _str.partition(".")
        parts2 = parts1[2].partition("s")
        parts3 = parts2[2].partition("e")
        
        show = parts1[0]

        season = -1
        if len(parts3[0]) == 2:
            try: season = int(parts3[0])
            except: pass
            
        episode = -1
        if len(parts3[2]) == 2:
            try: episode = int(parts3[2])
            except: pass
            
        return Url(show, season, episode)
    
class Urls(list):
    
    def filter(self, pattern):
        l = Urls()
        for url in self:
            if fnmatch.fnmatch(str(url), pattern):
                l.append(url)
        return l
    
    def filter_by_start(self, pattern):
        l = Urls()
        for url in self:
            if str(url).startswith(pattern):
                l.append(url)
        return l
    
    def to_str_list(self):
        ret = []
        for url in self:
            ret.append(str(url))
        return ret

    def find_by_url(self, _url):
        for url in self:
            if url.show == _url.show and url.season == _url.season and url.episode == _url.episode:
                return url
        return None
    
    def find_by_data(self, show, season, episode):
        for url in self:
            if url.show == show and url.season == season and url.episode == episode:
                return url
        return None
    
    def list_episodes(self):
        s = set()
        for url in self:
            s.add( "%s.s%02de%02d" % (url.show, url.season, url.episode) )
        return list(s)
    
    def list_seasons(self):
        s = set()
        for url in self:
            s.add( "%s.s%02d" % (url.show, url.season) )
        return list(s)
    
    def list_shows(self):
        s = set()
        for url in self:
            s.add( "%s." % (url.show) )
        return list(s)
        
