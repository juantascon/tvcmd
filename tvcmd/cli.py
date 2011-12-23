#! /usr/bin/env python

import readline, cmd
from tvcmd import cons, manager, torrent

import logging

def log():
    return logging.getLogger(__name__)

class Cmd(cmd.Cmd, manager.Manager):
    
    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        self.update_prompt()
        self.modified = False
        
    def update_prompt(self):
        self.prompt = "tvcmd:> "
    
    def do_shows(self, line):
        db = self.shows
        print("\n%s\n"%(db.fmt()))
    
    def do_search(self, line):
        db = self.search_show(line)
        print("\n%s\n"%(db.fmt()))
    
    def complete_tor(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
    
    def do_tor(self, line):
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE])
        
        for eurl in db:
            print(torrent.fmt_url(eurl["show"], eurl["season"], eurl["episode"]))
    
    def complete_adquire(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
        
    def do_adquire(self, line):
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE])
        
        if len(db): self.modified = True
        
        for eurl in db:
            eurl.update(status = cons.ADQUIRED)
            print(eurl.fmt_color())
            
    def complete_see(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE, cons.ADQUIRED])
        return db.complete_text(text)
    
    def do_see(self, line):
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE, cons.ADQUIRED])

        if len(db): self.modified = True
                
        for eurl in db:
            eurl.update(status = cons.SEEN)
            print(eurl.fmt_color())
    
    def complete_ls(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE, cons.ADQUIRED])
        return db.complete_text(text)
    
    def do_ls(self, line):
        db = self.episodes.filter(lambda url: url.match(line or "*") and url["status"] in [cons.NONE, cons.ADQUIRED])
        db.sort(key=lambda url: url["date"], reverse = True)
        
        for eurl in db:
            print(eurl.fmt_color())
    
    def do_save(self, line):
        try:
            log().info("saving ...")
            self.save()
            log().info("OK")
        except ConfigError as ex:
            log().info(ex)
    
    ## Basic commands:
        
    def exit(self):
        if self.modified:
            answer = input("Database has been modified. Do you want to save it now? [Y/n]: ")
            if not answer.lower().startswith("n"):
                try:
                    log().info("SAVING ...")
                    self.save()
                    log().info("OK")
                except ConfigError as ex:
                    log().info("FAIL (%s)"%(ex))
                    return False
        
        return True
    
    def emptyline(self):
        pass
    
    def do_exit(self, arg):
        return self.exit()
    
    def do_quit(self, arg):
        return self.exit()
    
    def do_EOF(self, arg):
        print()
        return self.exit()
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print()
            return self.exit()
