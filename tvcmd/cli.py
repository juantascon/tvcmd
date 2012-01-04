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
        readline.set_completer_delims(" ")
        
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        
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
        parser = ArgumentParser(prog="reload", description="Reload episodes list and status", epilog="example: reload")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
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
        parser = ArgumentParser(prog="save", description="Save episodes status DB", epilog="example: save")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        self.save()
    
    #
    # Show Commands
    #
    def do_shows(self, line):
        parser = ArgumentParser(prog="shows", description="List shows information", epilog="example: shows")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = self.show_db
        print("\n%s\n"%(db.fmt()))
    
    def do_search(self, line):
        parser = ArgumentParser(prog="shows", description="Search for shows in thetvdb.com database", epilog="example: search the office")
        parser.add_argument("filter", metavar="SHOW", help="show name or part, ex: the offi")
        try: args = parser.parse_args([line])
        except SystemExit: return
        
        msg("Searching [%s] ... "%(args.filter))
        try:
            db = self.search_shows(args.filter)
            msg("OK: %d shows found\n"%(len(db)))
            if (len(db)): print("\n%s\n"%(db.fmt()))
        except ServerError as ex:
            msg("FAIL: (%s)\n"%(ex))
    
    #
    # Complete text
    #
    def _complete(self, text, options, db):
        _options = [ opt for opt in options if opt.startswith(text) ]
        _episodes = db.complete_text(text)
        
        return _options + _episodes
    
    def complete_tor(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW]))
    
    def complete_ls(self, text, line, start_index, end_index):
        return self._complete(text, ["-n", "--new", "-a", "--adquired", "-s", "--seen", "-f", "--future"], self.episode_db)
    
    def complete_new(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.ADQUIRED, cons.SEEN]))
    
    def complete_adquire(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW]))
    
    def complete_see(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW, cons.ADQUIRED]))
    
    #
    # Episode Status Commands
    #
    def _mark(self, edb, status):
        msg("Marking %d episode(s) as %s:\n"%(len(edb), cons.ENUM_EPISODE_STATUS[status]))
        if len(edb): self.modified = True
        
        for eurl in edb:
            eurl.update(status = status)
            print(eurl.fmt_color())
    
    def do_new(self, line):
        parser = ArgumentParser(prog="new", description="Mark episodes as NEW", epilog="example: new lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = episode.DB()
        for pattern in args.filters:
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and not url.future() and url["status"] in [cons.ADQUIRED, cons.SEEN]))
        
        self._mark(db, cons.NEW)
    
    def do_adquire(self, line):
        parser = ArgumentParser(prog="adquire", description="Mark episodes as ADQUIRED", epilog="example: adquire lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = episode.DB()
        for pattern in args.filters:
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and not url.future() and url["status"] in [cons.NEW]))
        
        self._mark(db, cons.ADQUIRED)
    
    def do_see(self, line):
        parser = ArgumentParser(prog="see", description="Mark episodes as SEEN", epilog="example: see lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = episode.DB()
        for pattern in args.filters:
            db.extend(self.episode_db.filter(lambda url: url.match(pattern) and not url.future() and url["status"] in [cons.NEW, cons.ADQUIRED]))
        
        self._mark(db, cons.SEEN)
    
    #
    # Episode info Commands
    #
    def do_tor(self, line):
        parser = ArgumentParser(prog="tor", description="Show torrent urls for NEW episodes", epilog="example: tor lost*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = episode.DB()
        for pattern in args.filters:
            db.extend(self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW] and url.match(pattern)))
        
        for eurl in db:
            print(torrent.fmt_url(eurl["show"], eurl["season"], eurl["episode"]))
    
    def do_ls(self,line):
        parser = ArgumentParser(prog="ls", description="Show episodes information", epilog="example: ls -as lost*")
        parser.add_argument("-n", "--new", action="store_true", help="list NEW episodes (default)")
        parser.add_argument("-a", "--adquired", action="store_true", help="list ADQUIRED episodes (default)")
        parser.add_argument("-s", "--seen", action="store_true", help="list SEEN episodes")
        parser.add_argument("-f", "--future", action="store_true", help="list episodes not aired to date, implies -nas")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = episode.DB()
        for pattern in args.filters:
            db.extend(self.episode_db.filter(lambda url: url.match(pattern)))
        
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
    # Auxiliary commands:
    #
    def do_help(self, line):
        sep = "\n   "
        msg("To get specific help type: COMMAND --help\n\n")
        msg("Auxiliary commands:"+sep+sep.join(["exit", "quit", "help"]) + "\n")
        msg("DB commands:"+sep+sep.join(["save", "reload"]) + "\n")
        msg("Episodes commands:"+sep+sep.join(["new", "adquire", "see", "tor", "ls"]) + "\n")
        msg("Shows commands:"+sep+sep.join(["shows", "search"]) + "\n")
    
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
    
    def do_exit(self, line):
        parser = ArgumentParser(prog="exit/quit", description="Exit the application", epilog="example: exit")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        return self.exit()
    
    do_quit = do_exit
    
    def default(self, line):
        if line == "EOF":
            print()
            return self.exit()
        
        msg("Invalid command: %s"%(line.split(" ")[0]))
        return self.do_help("")
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("^C")
            return self.cmdloop()
