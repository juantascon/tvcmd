#! /usr/bin/env python

from tvcmd import cons, episode, show, config, thetvdb
from tvcmd.errors import (ServerError, ConfigError)

import sys
import logging

def log():
    return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.status = config.Status()
        self.main = config.Main()
        
        self.episodes = episode.DB()
        self.shows = show.DB()
    
    def load(self):
        # read status
        self.status.read()

        # read shows
        self.main.read()
        
        # sync status and shows
        for show in self.main.get_shows():
            self.track_show(show)
    
    def save(self):
        try:
            # sync status
            for eurl in self.episodes:
                if eurl["status"] == cons.NONE:
                    self.status.remove(eurl.url())
                else:
                    self.status.set(eurl.url(), eurl["status"])
                    
            # write status
            self.status.write()
        except Exception as ex: raise ConfigError("Error saving db (%s)"%(ex))
                    
    def search_show(self, show_name):
        log().info(" [%s]: SEARCHING ... "%(show_name))
        db = show.DB()
        try:
            for s in thetvdb.get_show_info(show_name):
                surl = show.Url(id=s["id"], name=s["name"], language=s["language"])
                db.append(surl)
        except ServerError as ex:
            log().info(" [%s]: FAIL (%s)" %(show_name, ex))
            
        log().info(" [%s]: %d item(s) FOUND" %(show_name, len(db)))
        return db
            
    def track_show(self, show_name):
        log().info(" [%s]: SEARCHING ... "%(show_name))
        try:
            s = thetvdb.get_show_info(show_name)[0]
            surl = show.Url(id=s["id"], name=s["name"], language=s["language"])
            
            log().info(" [%s]: TRACKING: %s ... "%(show_name, surl.fmt()))
            
            for d in thetvdb.get_episodes(s):
                eurl = episode.Url(show=d["show"], season=d["season"], episode=d["episode"], name=d["name"], date=d["date"])
                eurl.update(status = self.status.get(eurl.url()) or cons.NONE)
                self.episodes.append(eurl)
            
            self.shows.append(surl)
            log().info(" [%s]: OK"%(show_name))
        except ServerError as ex:
            log().info(" [%s]: FAIL (%s)" %(show_name, ex))
