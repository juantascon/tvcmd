import readline, cmd, argparse
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
        """Print tracked shows list\n\nSyntax:\n shows"""
        db = self.shows
        print("\n%s\n"%(db.fmt()))
    
    def do_search(self, line):
        """Search for shows in thetvdb.com database\n\nSyntax:\n search <TEXT>\nExample:\n search the_office"""
        db = self.search_show(line)
        print("\n%s\n"%(db.fmt()))
    
    def complete_adquire(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
        
    def do_adquire(self, line):
        """Mark episodes as ADQUIRED\n\nSyntax:\n adquire <EPISODE>\nExample:\n adquire lost.s01*"""
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE])
        
        if not len(db):
            print("episode list empty")
            return
        
        if len(db): self.modified = True
        
        for eurl in db:
            eurl.update(status = cons.ADQUIRED)
            print(eurl.fmt_color())
            
    def complete_see(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE, cons.ADQUIRED])
        return db.complete_text(text)
    
    def do_see(self, line):
        """Mark episodes as SEEN\n\nSyntax:\n see <EPISODE>\nExample:\n see lost.s01*"""
        db = self.episodes.filter(lambda url: url.match(line) and url["status"] in [cons.NONE, cons.ADQUIRED])
        
        if not len(db):
            print("episode list empty")
            return
            
        self.modified = True
        
        for eurl in db:
            eurl.update(status = cons.SEEN)
            print(eurl.fmt_color())
    
    def complete_tor(self, text, line, start_index, end_index):
        db = self.episodes.filter(lambda url: url["status"] in [cons.NONE])
        return db.complete_text(text)
    
    def do_tor(self, line):
        """Print torrent urls for NOT ADQUIRED episodes\n\nSyntax:\n tor [EPISODE]\nExample:\n tor *"""
        db = self.episodes.filter(lambda url: url.match(line or "*") and url["status"] in [cons.NONE])
        
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
    
    def do_save(self, line):
        """Save episodes status DB\n\nSyntax:\n save"""
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
        """Exit the application\n\nSyntax:\n exit"""
        return self.exit()
    
    def do_quit(self, arg):
        """Exit the application\n\nSyntax:\n quit"""
        return self.exit()
    
    def default(self, line):
        if line == "EOF":
            print()
            return self.exit()
        
        print()
        print("Invalid command: %s"%(line.split(" ")[0]))
        return self.do_help("")
    
    # def do_EOF(self, arg):
    #     print()
    #     return self.exit()
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("^C")
            return self.cmdloop()
