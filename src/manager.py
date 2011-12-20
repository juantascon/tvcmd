#! /usr/bin/env python

import thetvdb.api
import episode, config
import sys

class Manager():
    
    def __init__(self):
        self.cfg = config.Config()
        self.db = episode.DB()
        
    def load(self):
        self.cfg.load()
        
        for show in self.cfg.get_shows():
            sys.stdout.write("[%s]: " %(show))
            sys.stdout.flush()
            
            try:
                for d in thetvdb.api.get_episodes(show):
                    eurl = episode.Url(show=d["show"], season=d["season"], episode=d["episode"], name=d["name"], date=d["date"])
                    self.db.append(eurl)
                    try: eurl.update(status = self.cfg.get_status()[eurl.url()])
                    except KeyError: pass
                print("ok")
            except Exception as ex:
                print( "fail (%s)" % (ex) )
                
    def save(self):
        for eurl in self.db:
            if eurl["status"] == episode.STATUS_NONE:
                self.cfg.remove_status(eurl.url())
            else:
                self.cfg.set_status(eurl.url(), eurl["status"])
        self.cfg.save()
    
