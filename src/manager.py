#! /usr/bin/env python

import thetvdb.api
import episode
import sys

class Manager():
    
    def __init__(self, shows, seen):
        self.seen = episode.Urls()
        for s in seen:
            self.seen.append(episode.Url.parse(s))
        
        self.pending = episode.Urls()
        for show in shows:
            sys.stdout.write("[%s]: " %(show))
            sys.stdout.flush()
            try:
                for episode_str in thetvdb.api.get_episodes_list(show):
                    eurl = episode.Url.parse(episode_str)
                    if not self.seen.find_by_url(eurl):
                        self.pending.append(eurl)
                print("ok")
            except Exception as ex:
                print("fail (%s)"%(ex))

        
    def see(self, pattern):
        l = episode.Urls()
        for eurl in self.pending.filter(pattern):
            self.pending.remove(eurl)
            self.seen.append(eurl)
            l.append(eurl)
            
        return l
        
    def complete(self, text):
        urls = self.pending.filter_by_start(text)
        eurl = episode.Url.parse(text)
        
        # complete shows
        try: text.index(".")
        except: return urls.list_shows()
        
        # complete season
        if eurl.season == -1:
            return urls.list_seasons()
        
        # complete episodes
        if eurl.episode == -1:
            return urls.list_episodes()
        
        return []
