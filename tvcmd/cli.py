import readline, cmd, argparse
from tvcmd import cons, manager, torrent

from tvcmd.errors import (ServerError, ConfigError, TrackError)
from tvcmd import msg

import logging
def log(): return logging.getLogger(__name__)

class Cmd(cmd.Cmd, manager.Manager):
    
    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        self.update_prompt()
        self.modified = False
        
    def update_prompt(self):
        self.prompt = "tvcmd:> "
        
    def load(self):
        manager.Manager.load(self)
        
        for show_name in self.main.get_shows():
            msg("Tracking show %s ... "%(show_name))
            try:
                surl, edb = self.track(show_name)
                msg("OK: %d episodes found\n"%(len(edb)))
            except Exception as ex:
                msg("FAIL: (%s)\n"%(ex))
                
        self.modified = False
        
    def do_reload(self, line):
        """Reload episodes lists and reset their status\n\nSyntax:\n reload"""
        if self.modified:
            answer = self.ask_yn("Database has been modified. Are you sure you want to reload?")
            if not answer: return
            
        self.load()
        
    def do_shows(self, line):
        """Print tracked shows list\n\nSyntax:\n shows"""
        db = self.shows
        print("\n%s\n"%(db.fmt()))
    
    def do_search(self, line):
        """Search for shows in thetvdb.com database\n\nSyntax:\n search <TEXT>\nExample:\n search the_office"""
        msg("Searching [%s] ... "%(line))
        try:
            db = self.search_shows(line)
        except ServerError as ex: msg("FAIL: (%s)\n"%(ex))
        
        msg("OK: %d shows found\n"%(len(db)))
        print("\n%s\n"%(db.fmt()))
    
    def complete_adquire(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
        
    def do_adquire(self, line):
        """Mark episodes as ADQUIRED\n\nSyntax:\n adquire <EPISODE>\nExample:\n adquire lost.s01*"""
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE])
        
        msg("Marking %d episode(s) as ADQUIRED:\n"%(len(db)))
        
        if not len(db): return
        
        self.modified = True
        
        for eurl in db:
            eurl.update(status = cons.ADQUIRED)
            print(eurl.fmt_color())
            
    def complete_see(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE, cons.ADQUIRED])
        return db.complete_text(text)
    
    def do_see(self, line):
        """Mark episodes as SEEN\n\nSyntax:\n see <EPISODE>\nExample:\n see lost.s01*"""
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE, cons.ADQUIRED])
        
        msg("Marking %d episode(s) as SEEN:\n"%(len(db)))
        
        if not len(db): return
        
        self.modified = True
        
        for eurl in db:
            eurl.update(status = cons.SEEN)
            print(eurl.fmt_color())
    
    def complete_tor(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
    
    def do_tor(self, line):
        """Print torrent urls for NOT ADQUIRED episodes\n\nSyntax:\n tor [EPISODE]\nExample:\n tor *"""
        db = self.episodes.filter(lambda url: not url.future() and url.match(line or "*") and url["status"] in [cons.NONE])
        
        for eurl in db:
            print(torrent.fmt_url(eurl["show"], eurl["season"], eurl["episode"]))
    
    def complete_ls(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE, cons.ADQUIRED])
        return db.complete_text(text)
    
    def do_ls(self, line):
        """Show episodes information\n\nSyntax:\n ls [EPISODE]\nExample:\n ls *"""
        db = self.episodes.filter(lambda url: url.match(line or "*") and url["status"] in [cons.NONE, cons.ADQUIRED])
        db.sort(key=lambda url: url["date"], reverse = True)
        
        for eurl in db:
            print(eurl.fmt_color())

    def save(self):
        try:
            msg("Saving ... ")
            manager.Manager.save(self)
            msg("OK\n")
            self.modified = False
            return True
        except ConfigError as ex:
            msg("FAIL: (%s)\n"%(ex))
            return False
    
    def do_save(self, line):
        """Save episodes status DB\n\nSyntax:\n save"""
        self.save()
        
    ## Basic commands:
    def ask_yn(self, question):
        answer = ""
        while True:
            answer = input(question + " [y/n]: ").lower()
            if answer in ["y", "yes"]: return True
            elif answer in ["n", "no"]: return False
            
    def exit(self):
        if self.modified:
            answer = self.ask_yn("Database has been modified. Do you want to save it now?")
            if answer: return self.save()
        return True
    
    def emptyline(self):
        pass
    
    def do_exit(self, arg):
        """Exit the application\n\nSyntax:\n exit"""
        return self.exit()
    
    def do_quit(self, arg):
        """Exit the application\n\nSyntax:\n quit"""
        return self.exit()
    
    def default(self, line):
        print()
        
        if line == "EOF":
            return self.exit()
        
        msg("Invalid command: %s"%(line.split(" ")[0]))
        return self.do_help("")
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("^C")
            return self.cmdloop()
