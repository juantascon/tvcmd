import logging
def log(): return logging.getLogger(__name__)

#
# Shows and episodes are handled separately because it is easier to
# filter, in tvcmd a show is not a group episode, it is only
# a name and id used to get episodes lists from a source
# shows are represented in low case and _ charaters, ex:
# steins_gate, how_i_met_your_mother, the_office_us
#
class Item():
    
    # expected: id, name
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return self.url()
    
    def __eq__(self, other):
        return (self.id == other.id)
    
    def fmt(self):
        return "[ %s ]: %s" % (self.id, self.url())
    
    def url(self):
        return self.name.replace("(","").replace(")","").replace(" ", "_").lower()
    
class List(list):
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def fmt(self):
        return "\n".join([ s.fmt() for s in self ])
        
    def filter(self, function):
        return List(item for item in self if function(item))
