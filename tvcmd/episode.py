import fnmatch, datetime

from . import cons

import logging
def log(): return logging.getLogger(__name__)

#
# Episode URL is a string that follow this pattern: ${showname}.s${seasonnumber%d2}e${episodenumber%d2},ex:
# lost.s01e03, how_i_met_your_mother.s09e18, community.s05e07
#
class Item():
    
    def __init__(self, show, season=None, episode=None, name=None, date=None, status=None):
        self.show = show
        self.season = season
        self.episode = episode
        self.name = name
        self.date = date
        self.status = status
    
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
        
        return color + "%s : [ %s ] [ %s ]" % (self.url(), str(self.date), self.name) + COLOR_END
        
    def match(self, pattern):
        return fnmatch.fnmatch(self.url(), pattern)
    
    def startswith(self, pattern):
        return self.url().startswith(pattern)
    
    def future(self):
        try:
            if self.date < datetime.date.today():
                return False
        except: pass
        
        return True
        
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
