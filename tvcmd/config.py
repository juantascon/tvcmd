#! /usr/bin/env python

import os, configparser

import logging

def log():
    return logging.getLogger(__name__)

class Config():
    
    DIR = os.environ["XDG_CONFIG_HOME"]+"/tvcmd/"
    
    def __init__(self):
        self.main = configparser.ConfigParser()
        self.status = configparser.ConfigParser()
        
    def load(self):
        self.main.read(self.DIR+"main.cfg")
        self.status.read(self.DIR+"status.cfg")
        
        try: self.main.add_section("general")
        except: pass
        
        try: self.status.add_section("status")
        except: pass
        
    def get_status(self):
        d = {}
        for s in self.status.items("status"):
            d[s[0]] = int(s[1])
        return d
        
    def set_status(self, eurl, status):
        self.status.set("status", eurl, str(status))
        
    def remove_status(self, eurl):
        self.status.remove_option("status", eurl)
    
    def get_shows(self):
        l = []
        for s in self.main.get("general", "shows", fallback="").split(","):
            s = s.strip()
            if len(s) > 0: l.append(s)
        return l
    
    def save(self):
        try: os.makedirs(self.DIR)
        except: pass
        
        self.status.write(open(self.DIR+"status.cfg", "w"))
        
