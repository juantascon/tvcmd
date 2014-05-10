import logging
def log(): return logging.getLogger(__name__)

#
# Shows and episodes are handled separately because that way is
# easier to filter episodes, in tvcmd a show is not a group of episodes,
# it is only a set of name, realname and id used to get episodes lists
# from a source, shows name are represented in low case and _ charaters,
# ex: steins_gate, how_i_met_your_mother, the_office_us
#
class Item():
    
    def __init__(self, realname, id=0):
        self.name = self.flatname(realname)
        self.realname = realname
        self.id = id or 0
    
    def __eq__(self, other):
        return (self.url() == other.url())
    
    def url(self):
        return self.name
        
    def print_str(self):
        return "%s : [ %s ] [ %s ]" % (self.url(), self.realname, self.id)
    
    @classmethod
    def flatname(cls, _str):
        ret = _str.replace("(", "").replace(")", "")
        ret = ret.replace(":", "_").replace(";", "_").replace(",", "_").replace(".", "_")
        ret = ret.replace("'", "")
        ret = ret.replace("-", "").replace(" ", "_")
        
        while "__" in ret:
            ret = ret.replace("__", "_")
        
        return ret.lower()
    
class List(list):
    
    def upsert(self, s):
        for item in self:
            if item == s:
                item.realname = s.realname
                item.id = s.id
                return
        self.append(s)
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def print_str(self):
        return "\n".join([ s.print_str() for s in self ])
        
    def filter(self, function):
        return List(item for item in self if function(item))
