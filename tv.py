#! /usr/bin/env python2

import tvdb_api, tvdb_exceptions
import fnmatch
import sys

db = tvdb_api.Tvdb()

class EpisodeUrl():
    
    COLOR_PENDING = "\033[31m"
    COLOR_SEEN = "\033[32m"
    COLOR_FUTURE = "\033[33m"
    COLOR_END = "\033[0m"
    
    def __init__(self, show, season, episode):
        self.show = show
        self.season = season
        self.episode = episode
        
    def fmt(self):
        try: name = db[self.show][self.season][self.episode]["episodename"]
        except: name = "N/A"
        
        try: date = db[self.show][self.season][self.episode]["firstaired"]
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
            
        return EpisodeUrl(show, season, episode)
    
class EpisodeUrlList(list):
    
    def filter(self, pattern):
        l = EpisodeUrlList()
        for eurl in self:
            if fnmatch.fnmatch(str(eurl), pattern):
                l.append(eurl)
        return l
    
    def filter_by_start(self, pattern):
        l = EpisodeUrlList()
        for eurl in self:
            if str(eurl).startswith(pattern):
                l.append(eurl)
        return l
    
    def to_str_list(self):
        ret = []
        for eurl in self:
            ret.append(str(eurl))
        return ret
    
    def find_by_data(self, show, season, episode):
        for eurl in self:
            if eurl.show == show and eurl.season == season and eurl.episode == episode:
                return eurl
        return None
    
    def list_episodes(self):
        s = set()
        for eurl in self:
            s.add( "%s.s%02de%02d" % (eurl.show, eurl.season, eurl.episode) )
        return list(s)
    
    def list_seasons(self):
        s = set()
        for eurl in self:
            s.add( "%s.s%02d" % (eurl.show, eurl.season) )
        return list(s)
    
    def list_shows(self):
        s = set()
        for eurl in self:
            s.add( "%s." % (eurl.show) )
        return list(s)
        
class Manager():
    
    def __init__(self, shows, seen):
        self.seen = EpisodeUrlList()
        for s in seen:
            self.seen.append(EpisodeUrl.parse(s))
        
        self.pending = EpisodeUrlList()
        for show in shows:
            sys.stdout.write("[%s]: " %(show))
            sys.stdout.flush()
            try: 
                for season in db[show]:
                    for episode in db[show][season]:
                        if not self.seen.find_by_data(show, season, episode):
                            self.pending.append(EpisodeUrl(show, season, episode))
                print("ok")
            except tvdb_exceptions.tvdb_error as ex:
                print("fail (%s)"%(ex))

        
    def see(self, pattern):
        l = EpisodeUrlList()
        for eurl in self.pending.filter(pattern):
            self.pending.remove(eurl)
            self.seen.append(eurl)
            l.append(eurl)
            
        return l
        
    def complete(self, text):
        urls = self.pending.filter_by_start(text)
        eurl = EpisodeUrl.parse(text)
        
        # complete shows
        try: text.index(".")
        except: return urls.list_shows()
        
        # complete season
        if eurl.season == -1:
            return urls.list_seasons()
        
        # complete episodes
        if eurl.episode == -1:
            return urls.list_episodes()
        
        return []
