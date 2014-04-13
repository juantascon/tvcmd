import fnmatch, datetime

from . import cons

import logging
def log(): return logging.getLogger(__name__)

#
# Episode URL is a string that follow this pattern: ${showname}.s${seasonnumber%d2}e${episodenumber%d2},ex:
# lost.s01e03, how_i_met_your_mother.s09e18, community.s05e07
#
class Item():
    
    def __init__(self, show="", season=0, episode=0, name="", date=str(datetime.date.max), status=cons.NEW):
        self.show = show or ""
        self.season = season or 0
        self.episode = episode or 0
        self.name = name or ""
        
        self.date = date or str(datetime.date.max)
        self.status = status or cons.NEW
    
    def to_dict(self):
        return { "url": self.url(), "date": self.date, "name": self.name, "status": self.status }
    
    def url(self):
        return self.str_show() + self.str_season() + self.str_episode()
    
    def __eq__(self, other):
        return (self.url() == other.url())
        
    def str_episode(self):
        try: return ( "e%02d" %(self.episode) )
        except KeyError: return ""
    
    def str_season(self):
        try: return ( "s%02d" %(self.season) )
        except KeyError: return ""
    
    def str_show(self):
        try: return ( self.show + "." )
        except KeyError: return ""
    
    def format(self, fmt):
        fmt = fmt.replace("${show}", self.show)
        fmt = fmt.replace("${show+}", self.show.replace("_", "+"))
        fmt = fmt.replace("${season}", "%02d" % self.season)
        fmt = fmt.replace("${episode}", "%02d" % self.episode)
        return fmt
    
    def print_str(self):
        COLOR_END = "\033[0m"
        
        if self.future(): color = cons.ENUM_EPISODE_STATUS[cons.FUTURE]["color"]
        else: color = cons.ENUM_EPISODE_STATUS[self.status]["color"]
        
        status_text = cons.ENUM_EPISODE_STATUS[self.status]["text"]
        
        return color + "%s : [ %s ] [ %s ] [ %s ]" % (self.url(), status_text, self.date, self.name) + COLOR_END
        
    def match(self, pattern):
        return fnmatch.fnmatch(self.url(), pattern)
    
    def startswith(self, pattern):
        return self.url().startswith(pattern)
    
    def future(self):
        try:
            if datetime.datetime.strptime(self.date, "%Y-%m-%d").date() < datetime.date.today():
                return False
        except: pass
        
        return True
    
    @classmethod
    def new_from_dict(cls, _dict):
        # use ether url or independent fields
        if _dict.get("url") is None:
            e = Item(_dict.get("show"), _dict.get("season"), _dict.get("episode"))
        else:
            e = Item.new_from_url(_dict.get("url"))
        
        e.name = _dict.get("name") or ""
        e.date = _dict.get("date") or str(datetime.date.max)
        e.status = _dict.get("status") or cons.NEW
        
        return e
    
    @classmethod
    def new_from_url(cls, _str):
        parts1 = _str.partition(".")
        parts2 = parts1[2].partition("s")
        parts3 = parts2[2].partition("e")
        
        show = parts1[0]
        
        e = Item(show)
        
        if len(parts3[0]) == 2:
            try: e.season = int(parts3[0])
            except: pass
            
        if len(parts3[2]) == 2:
            try: e.episode = int(parts3[2])
            except: pass
            
        return e
    
class List(list):
    
    def upsert_r(self, items):
        for i in items:
            self.upsert(i)
    
    #
    # updates/inserts an element, on update status is kept untouched
    #
    def upsert(self, e):
        for item in self:
            if item.url() == e.url():
                item.name = e.name
                item.date = e.date
                return
        self.append(e)
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def filter(self, function):
        return List(item for item in self if function(item))
    
    def complete_text(self, text):
        l = self.filter(lambda e: e.startswith(text))
        e = Item.new_from_url(text)
        
        # complete shows
        try: text.index(".")
        except: return l.list_shows()
        
        # complete season
        if not e.season: return l.list_seasons()
        
        # complete episodes
        if not e.episode: return l.list_episodes()
        
        # nothing to complete
        return []
    
    def list_episodes(self):
        s = set()
        for e in self:
            s.add( e.str_show() + e.str_season() + e.str_episode() )
        return list(s)
    
    def list_seasons(self):
        s = set()
        for e in self:
            s.add( e.str_show() + e.str_season() )
        return list(s)
    
    def list_shows(self):
        s = set()
        for e in self:
            s.add( e.str_show() )
        return list(s)
        
    def print_str(self):
        return "\n".join([ e.print_str() for e in self ])
