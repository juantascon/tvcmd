#! /usr/bin/env python2

import readline, cmd
import torrent, episode, manager

class Cmd(cmd.Cmd, manager.Manager):

    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        
    def load(self):
        manager.Manager.load(self)
    
    def do_shows(self, line):
        print(self.db.list_shows())

    def complete_tor(self, text, line, start_index, end_index):
        subdb = self.db.filter(lambda url: url["status"] in [episode.STATUS_NONE])
        return subdb.complete_text(text)
    
    def do_tor(self, line):
        subdb = self.db.filter(lambda url: url.match(line) and url["status"] in [episode.STATUS_NONE])
        
        for eurl in subdb:
            print(torrent.fmt_url(eurl["show"], eurl["season"], eurl["episode"]))
    
    def complete_adquire(self, text, line, start_index, end_index):
        subdb = self.db.filter(lambda url: url["status"] in [episode.STATUS_NONE])
        return subdb.complete_text(text)
        
    def do_adquire(self, line):
        subdb = self.db.filter(lambda url: url.match(line) and url["status"] in [episode.STATUS_NONE])
        
        for eurl in subdb:
            eurl.update(status = episode.STATUS_ADQUIRED)
            print(eurl.fmt_color())
            
    def complete_see(self, text, line, start_index, end_index):
        subdb = self.db.filter(lambda url: url["status"] in [episode.STATUS_NONE, episode.STATUS_ADQUIRED])
        return subdb.complete_text(text)
    
    def do_see(self, line):
        subdb = self.db.filter(lambda url: url.match(line) and url["status"] in [episode.STATUS_NONE, episode.STATUS_ADQUIRED])
        
        for eurl in subdb:
            eurl.update(status = episode.STATUS_SEEN)
            print(eurl.fmt_color())
    
    def complete_ls(self, text, line, start_index, end_index):
        subdb = self.db.filter(lambda url: url["status"] in [episode.STATUS_NONE, episode.STATUS_ADQUIRED])
        return subdb.complete_text(text)
    
    def do_ls(self, line):
        subdb = self.db.filter(lambda url: url.match(line or "*") and url["status"] in [episode.STATUS_NONE, episode.STATUS_ADQUIRED])
        subdb.sort(key=lambda url: url["date"], reverse = True)
        
        for eurl in subdb:
            print(eurl.fmt_color())
    
    def do_save(self, line):
        self.save()
    
    ## Basic commands:
    
    def emptyline(self):
        pass
    
    def do_exit(self, arg):
        return True
        
    def do_quit(self, arg):
        return True
        
    def do_EOF(self, arg):
        print()
        return True
        
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print()
            return True
