import readline, cmd, argparse, sys
from tvcmd import episode, show, cons, manager, torrent

from tvcmd.errors import (ServerError, ConfigError, TrackError)
from tvcmd import msg

import logging
def log(): return logging.getLogger(__name__)

class ArgumentParser(argparse.ArgumentParser):
    
    def _print_message(self, message, file=None):
        if message:
            msg(message)
            
class Cmd(cmd.Cmd, manager.Manager):
    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        
        readline.set_completer_delims(readline.get_completer_delims().replace("-", ""))
        
        self.update_prompt()
        self.modified = False
        
    def update_prompt(self):
        self.prompt = "tvcmd:> "
    
    #
    # DB IO commands
    #
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
    
    #
    # Show Commands
    #
    def do_shows(self, line):
        """Print tracked shows list\n\nSyntax:\n shows"""
        db = self.show_db
        print("\n%s\n"%(db.fmt()))
    
    def do_search(self, line):
        """Search for shows in thetvdb.com database\n\nSyntax:\n search <TEXT>\nExample:\n search the office"""
        msg("Searching [%s] ... "%(line))
        try:
            db = self.search_shows(line)
        except ServerError as ex: msg("FAIL: (%s)\n"%(ex))
        
        msg("OK: %d shows found\n"%(len(db)))
        print("\n%s\n"%(db.fmt()))

    #
    # Episode Status Commands
    #
    def complete_new(self, text, line, start_index, end_index):
        db = self.episode_db.filter(lambda url: url["status"] in [cons.ADQUIRED, cons.SEEN])
        return db.complete_text(text)
    
    def complete_adquire(self, text, line, start_index, end_index):
        db = self.episode_db.filter(lambda url: url["status"] in [cons.NEW])
        return db.complete_text(text)
    
    def complete_see(self, text, line, start_index, end_index):
        db = self.episode_db.filter(lambda url: url["status"] in [cons.NEW, cons.ADQUIRED])
        return db.complete_text(text)
    
    def mark(self, edb, status):
        msg("Marking %d episode(s) as %s:\n"%(len(edb), cons.ENUM_EPISODE_STATUS[status]))
        if len(edb): self.modified = True
        
        for eurl in edb:
            eurl.update(status = status)
            print(eurl.fmt_color())
    
    def do_new(self, line):
        """Mark episodes as NEW\n\nSyntax:\n new <EPISODE> ... \nExample:\n new lost.s01* lost.s02*"""
        db = episode.DB()
        for pattern in line.split(" "):
            if not pattern: continue
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and url["status"] in [cons.ADQUIRED, cons.SEEN]))
        
        self.mark(db, cons.NEW)
    
    def do_adquire(self, line):
        """Mark episodes as ADQUIRED\n\nSyntax:\n adquire <EPISODE> ... \nExample:\n adquire lost.s01* lost.s02*"""
        db = episode.DB()
        for pattern in line.split(" "):
            if not pattern: continue
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and url["status"] in [cons.NEW]))
        
        self.mark(db, cons.ADQUIRED)
    
    def do_see(self, line):
        """Mark episodes as SEEN\n\nSyntax:\n see <EPISODE> ...\nExample:\n see lost.s01* lost.s02*"""
        db = episode.DB()
        for pattern in line.split(" "):
            if not pattern: continue
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and url["status"] in [cons.NEW, cons.ADQUIRED]))
        
        self.mark(db, cons.SEEN)
    
    #
    # Episode info Commands
    #
    def complete_tor(self, text, line, start_index, end_index):
        db = self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW])
        return db.complete_text(text)
    
    def do_tor(self, line):
        """Print torrent urls for NEW episodes\n\nSyntax:\n tor [EPISODE] ...\nExample:\n tor lost.s02* the_offi*"""
        if not line: line = "*"
        
        db = episode.DB()
        for pattern in line.split(" "):
            if not pattern: continue
            db.extend(self.episode_db.filter(lambda url: not url.future() and url.match(pattern) and url["status"] in [cons.NEW]))
        
        for eurl in db:
            print(torrent.fmt_url(eurl["show"], eurl["season"], eurl["episode"]))
    
    def complete_ls(self, text, line, start_index, end_index):
        db = self.episode_db
        episodes = db.complete_text(text)
        
        options = ["-n", "--new", "-a", "--adquired", "-s", "--seen", "-f", "--future"]
        options = [ opt for opt in options if opt.startswith(text) ]
        
        return  episodes + options
    
    def do_ls(self,line):
        parser = ArgumentParser(prog="ls", description="Show episodes information", epilog="example: ls -as lost*")
        parser.add_argument("-n", "--new", action="store_true", help="list NEW episodes (default)")
        parser.add_argument("-a", "--adquired", action="store_true", help="list ADQUIRED episodes (default)")
        parser.add_argument("-s", "--seen", action="store_true", help="list SEEN episodes")
        parser.add_argument("-f", "--future", action="store_true", help="list episodes not aired to date, implies -nas")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = self.episode_db
        for pattern in args.filters:
            db = db.filter(lambda url: url.match(pattern))
        
        # defaults: NEW and ADQUIRED
        if not (args.new or args.adquired or args.seen or args.future):
            args.new = args.adquired = True
        
        # future implies every other status
        if args.future:
            db = db.filter( lambda url: url.future() )
            args.new = args.adquired = args.seen = True
        else:
            db = db.filter( lambda url: not url.future() )
        
        if not args.new: db = db.filter( lambda url: url["status"] != cons.NEW )
        if not args.adquired: db = db.filter( lambda url: url["status"] != cons.ADQUIRED )
        if not args.seen: db = db.filter( lambda url: url["status"] != cons.SEEN )
        
        db.sort(key=lambda url: url["date"], reverse = True)
        
        for eurl in db:
            print(eurl.fmt_color())
    
    #
    # Exit commands:
    #
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
