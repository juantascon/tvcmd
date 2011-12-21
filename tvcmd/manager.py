#! /usr/bin/env python

from tvcmd import episode, config, thetvdb
import sys
import logging

def log():
    return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.cfg = config.Config()
        self.db = episode.DB()
        
    def load(self):
        self.cfg.load()
        
        for show in self.cfg.get_shows():
            log().info("[%s]: loading"%(show))
            try:
                for d in thetvdb.get_episodes(show):
                    eurl = episode.Url(show=d["show"], season=d["season"], episode=d["episode"], name=d["name"], date=d["date"])
                    try: eurl.update(status = self.cfg.get_status()[eurl.url()])
                    except KeyError: eurl.update(status = episode.STATUS_NONE)
                    
                    self.db.append(eurl)
                log().info("[%s]: OK"%(show))
            except Exception as ex:
                log().info("[%s]: FAIL" %(show))
                raise ex
                
    def save(self):
        for eurl in self.db:
            if eurl["status"] == episode.STATUS_NONE:
                self.cfg.remove_status(eurl.url())
            else:
                self.cfg.set_status(eurl.url(), eurl["status"])
        self.cfg.save()
    
