import logging
def log(): return logging.getLogger(__name__)

class Url(dict):
    
    # expected: id, name
    def __init__(self, **kwargs):
        self.update(**kwargs)
    
    def __repr__(self):
        return self.url()
    
    def __eq__(self, other):
        return (self["id"] == other["id"])
    
    def update(self, **kwargs):
        for key,value in kwargs.items():
            self[key] = value
    
    def fmt(self):
        return "[ %s ]: %s" % (self["id"], self.url())
    
    def url(self):
        return self["name"].replace("(","").replace(")","").replace(" ", "_").lower()
    
class DB(list):
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def fmt(self):
        return "\n".join([ url.fmt() for url in self ])
        
    def update(self, **kwargs):
        for url in self:
            url.update(**kwargs)
    
    def filter(self, function):
        return DB(item for item in self if function(item))
