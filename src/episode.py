#! /usr/bin/env python

import thetvdb.api
import fnmatch

COLOR_PENDING = "\033[31m"
COLOR_SEEN = "\033[32m"
COLOR_END = "\033[0m"
#COLOR_FUTURE = "\033[33m"

STATUS_NONE = 0
STATUS_ADQUIRED = 1
STATUS_SEEN = 2

class Url(dict):    
    
    # expected: show, season, episode, name, date, status
    def __init__(self, **kwargs):
        self["status"] = STATUS_NONE
        for key,value in kwargs.items():
            self[key] = value
        
    def update(self, **kwargs):
        for key,value in kwargs.items():
            self[key] = value
    
    def fmt(self):
        return "%s : [ %s ] [ %s ]" % (self.url(), self["date"], self["name"])
        
    def fmt_color(self):
        return (COLOR_SEEN if self["status"] == STATUS_SEEN else COLOR_PENDING) + self.fmt() + COLOR_END
    
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
    
    def __eq__(self, other):
        return (self.url() == other.url())
        
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

    def __repr__(self):
        s = ""
        for url in self:
            s = s+url.url() + "\n"
        return s
    
    def update(self, **kwargs):
        for url in self:
            url.update(kwargs)
    
    def filter_by_url_pattern(self, pattern):
        db = DB()
        for url in self:
            if fnmatch.fnmatch(url.url(), pattern):
                db.append(url)
        return db
    
    def filter_by_url_startswith(self, pattern):
        db = DB()
        for url in self:
            if url.url().startswith(pattern):
                db.append(url)
        return db
    
    # usage result = filter(show="lost", season=1)
    def filter(self, **kwargs):
        db = DB()
        for item in self:
            for key,value in kwargs.items():
                try:
                    if item[key] == value:
                        db.append(item)
                    else:
                        break
                except KeyError:
                    break
        return db
    
    def to_str_list(self):
        l = []
        for url in self:
            l.append(url.url())
        return l
    
    def complete_text(self, text):
        urls = self.filter_by_url_startswith(text)
        eurl = Url.parse(text)
        
        # complete shows
        try: text.index(".")
        except: return urls.list_shows()
        
        # complete season
        try: eurl["season"]
        except KeyError: return urls.list_seasons()
        
        # complete episodes
        try: eurl["episode"]
        except KeyError: return urls.list_episodes()
        
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
        
