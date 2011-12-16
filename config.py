#! /usr/bin/env python2

import os, json

CONFIG_DIR = os.environ["XDG_CONFIG_HOME"]+"/pyepisodes/"

try: os.makedirs(CONFIG_DIR)
except: pass

class Config():
    def __init__(self, path, data):
        self.path = path
        self.data = data
        
        try: f = open(self.path, "r+")
        except: f = open(self.path, "w+")
        
        f.close()
    
    def save(self):
        f = open(self.path, "w+")
        try: f.write(str(json.dumps(self.data, indent=1, separators=(',',':'))+"\n"))
        except: pass
        f.close()
    
    def load(self):
        f = open(self.path, "r+")
        try: self.data.extend(json.loads(f.read()))
        except: pass
        f.close()

SHOWS = Config(CONFIG_DIR+"shows.db", [])
SHOWS.load()

SEEN = Config(CONFIG_DIR+"seen.db", [])
SEEN.load()
