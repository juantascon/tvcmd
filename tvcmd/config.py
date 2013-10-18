from . import cons, errors

import os, configparser

import logging
def log(): return logging.getLogger(__name__)

class ConfigFileParser(configparser.ConfigParser):
    
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
    def read(self):
        return super().read(self.filename)
        
    def write(self):
        try: os.makedirs(os.path.dirname(self.filename))
        except: pass
        
        with open(self.filename, "w") as f:
            return super().write(f)


class Status(ConfigFileParser):
    
    def __init__(self):
        super().__init__(cons.STATUSDBFILE)
        
    def read(self):
        super().read()
        try: self.add_section("status")
        except: pass

    def get(self, eurl):
        try: return int(super().get("status", eurl))
        except: return None
        
    def get_all(self):
        d = {}
        for s in self.items("status"):
            d[s[0]] = int(s[1])
        return d
    
    def set(self, eurl, status):
        super().set("status", eurl, str(status))
        
    def remove(self, eurl):
        self.remove_option("status", eurl)
    

class Main(ConfigFileParser):
    
    def __init__(self):
        super().__init__(cons.MAINCONFIGFILE)
        
    def read(self):
        super().read()
        try: self.add_section("general")
        except: pass
        
    def get_shows(self):
        l = []
        for s in self.get("general", "shows", fallback="").split(","):
            s = s.strip()
            if len(s) > 0: l.append(s)
        return l
        
    def get_formats(self):
        l = []
        for s in self.get("general", "formats", fallback="").split(","):
            s = s.strip()
            if len(s) > 0: l.append(s)
        return l
        
    def get_source(self):
        _source = self.get("general", "source", fallback="thetvdb")
        
        if _source not in ["thetvdb", "tvrage"]:
             raise errors.ConfigError("Invalid source: %s" %(_source))
        
        return _source
        