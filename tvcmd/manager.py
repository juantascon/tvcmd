#! /usr/bin/env python

from tvcmd import errors, episode, config, thetvdb
from tvcmd.errors import (ServerError)
import sys
import logging

def log():
    return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        
        self.db = episode.DB()
        self.shows = []
    
    def load(self):
        # read status and shows
        self.status.read()
        self.main.read()
        
        # load
        for show in self.main.get_shows():
            self.add_show(show)
    
    def save(self):
        # sync status
        for eurl in self.db:
            if eurl["status"] == episode.STATUS_NONE:
                self.status.remove(eurl.url())
            else:
                self.status.set(eurl.url(), eurl["status"])
        
        # sync shows
        for show in self.shows:
            self.main.add_show(show)
        
        # write both
        self.main.write()
        self.status.write()
    
    def add_show(self, show):
        log().info(" show[%s]: loading ... "%(show))
        try:
            for d in thetvdb.get_episodes(show):
                eurl = episode.Url(show=d["show"], season=d["season"], episode=d["episode"], name=d["name"], date=d["date"])
                eurl.update(status = self.status.get(eurl.url()) or episode.STATUS_NONE)
                self.db.append(eurl)
            
            self.shows.append(show)
            log().info(" show[%s]: OK"%(show))
        except ServerError as ex:
            log().info(" show[%s]: FAIL (%s)" %(show, ex))
