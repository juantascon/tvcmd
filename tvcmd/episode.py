#! /usr/bin/env python

import fnmatch, datetime

from tvcmd import cons

class Url(dict):
    
    # expected: show, season, episode, name, date, status
    def __init__(self, **kwargs):
        self.update(**kwargs)
    
    def __repr__(self):
        return self.url()
    
    def __eq__(self, other):
        return (self.url() == other.url())
    
    def update(self, **kwargs):
        for key,value in kwargs.items():
            self[key] = value
    
    def fmt(self):
        return "%s : [ %s ] [ %s ]" % (self.url(), str(self["date"]), self["name"])
    
    def match(self, pattern):
        return fnmatch.fnmatch(self.url(), pattern)
    
    def startswith(self, pattern):
        return self.url().startswith(pattern)
    
    def future(self):
        try:
            if self["date"] < datetime.date.today():
                return False
        except: pass
        
        return True
        
    def fmt_color(self):
        COLOR_NONE = "\033[31m"
        COLOR_ADQUIRED = "\033[33m"
        COLOR_SEEN = "\033[32m"
        #COLOR_FUTURE = "\033[41m"
        COLOR_FUTURE = "\033[30m"
        COLOR_END = "\033[0m"
        
        color = COLOR_NONE
        if self["status"] == cons.ADQUIRED: color = COLOR_ADQUIRED
        if self["status"] == cons.SEEN: color = COLOR_SEEN
        if self.future(): color = COLOR_FUTURE
        
        return color + self.fmt() + COLOR_END
    
    def fmt_episode(self):
        try: return ( "e%02d" %(self["episode"]) )
        except KeyError: return ""
    
    def fmt_season(self):
        try: return ( "s%02d" %(self["season"]) )
        except KeyError: return ""
    
    def fmt_show(self):
        try: return ( self["show"] + "." )
        except KeyError: return ""
        
    def url(self):
        return self.fmt_show() + self.fmt_season() + self.fmt_episode()
    
    @classmethod
    def parse(cls, _str):
        parts1 = _str.partition(".")
        parts2 = parts1[2].partition("s")
        parts3 = parts2[2].partition("e")
        
        show = parts1[0]
        
        url = Url(show = show)
        
        if len(parts3[0]) == 2:
            try: url.update(season = int(parts3[0]))
            except: pass
            
        if len(parts3[2]) == 2:
            try: url.update(episode = int(parts3[2]))
            except: pass
            
        return url
    
class DB(list):
    
    def update(self, **kwargs):
        for url in self:
            url.update(**kwargs)
    
    def filter(self, function):
        return DB(item for item in self if function(item))
    
    def complete_text(self, text):
        subdb = self.filter(lambda url: url.startswith(text))
        eurl = Url.parse(text)
        
        # complete shows
        try: text.index(".")
        except: return subdb.list_shows()
        
        # complete season
        try: eurl["season"]
        except KeyError: return subdb.list_seasons()
        
        # complete episodes
        try: eurl["episode"]
        except KeyError: return subdb.list_episodes()
        
        return []
    
    def list_episodes(self):
        s = set()
        for url in self:
            s.add( url.fmt_show() + url.fmt_season() + url.fmt_episode() )
        return list(s)
    
    def list_seasons(self):
        s = set()
        for url in self:
            s.add( url.fmt_show() + url.fmt_season() )
        return list(s)
    
    def list_shows(self):
        s = set()
        for url in self:
            s.add( url.fmt_show() )
        return list(s)
    
