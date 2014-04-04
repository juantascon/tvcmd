import readline, cmd, argparse
from . import manager, episode, show, cons, errors

from . import __version__

import logging
def log(): return logging.getLogger(__name__)

class ArgumentParser(argparse.ArgumentParser):    
    def _print_message(self, message, file=None):
        if message:
            print(message)

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
        try:
            manager.Manager.load(self)
        except errors.ConfigError as ex:
            print("Error loading: %s" % (ex))
        
        self.modified = False
        
    def do_reload(self, line):
        parser = ArgumentParser(prog="reload", description="Reload episodes list and status", epilog="example: reload")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        if self.modified:
            answer = self.ask_yn("Status database has been modified. Are you sure you want to reload?")
            if not answer: return
            
        self.load()
        
    def do_update(self, line):
        parser = ArgumentParser(prog="update", description="Updates episodes from source", epilog="example: upload")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        for show_name in self.main.get_shows():
            print("Tracking show %s ... "%(show_name), end="")
            try:
                l = self.track(show_name)
                print("OK: %d episodes found"%(len(l)))
            except Exception as ex:
                print("FAIL: (%s)"%(ex))
        
        try:
            print("Saving cache ... ", end="")
            self.save_cache()
            print("OK")
        except Exception as ex:
            print("FAIL: (%s)"%(ex))
    
    def save(self):
        try:
            print("Saving ... ", end="")
            self.save_status()
            print("OK")
            self.modified = False
            return True
        except errors.ConfigError as ex:
            print("FAIL: (%s)"%(ex))
            return False
    
    def do_save(self, line):
        parser = ArgumentParser(prog="save", description="Save episodes status DB and cache", epilog="example: save")
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
        
        l = self.shows
        print(l.print_str())
    
    def do_search(self, line):
        parser = ArgumentParser(prog="shows", description="Search for shows in thetvdb.com database", epilog="example: search the office")
        parser.add_argument("filter", metavar="SHOW", help="show name or part, ex: the offi")
        try: args = parser.parse_args([line])
        except SystemExit: return
        
        print("Searching [%s] ... "%(args.filter), end="")
        try:
            l = self.search_shows(args.filter)
            print("OK: %d shows found"%(len(l)))
            if (len(l)): print("\n"+l.print_str())
        except Exception as ex:
                print("FAIL: (%s)"%(ex))
    
    #
    # Complete text
    #
    def _complete(self, text, options, elist):
        _options = [ opt for opt in options if opt.startswith(text) ]
        _episodes = elist.complete_text(text)
        
        return _options + _episodes
    
    def complete_format(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episodes.filter(lambda e: not e.future() and e.status in [cons.NEW]))
    
    def complete_ls(self, text, line, start_index, end_index):
        return self._complete(text, ["-n", "--new", "-a", "--adquired", "-s", "--seen", "-f", "--future"], self.episodes)
    
    def complete_new(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episodes.filter(lambda e: not e.future() and e.status in [cons.ADQUIRED, cons.SEEN]))
    
    def complete_adquire(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episodes.filter(lambda e: not e.future() and e.status in [cons.NEW]))
    
    def complete_see(self, text, line, start_index, end_index):
        return self._complete(text, ["-h", "--help"], self.episodes.filter(lambda e: not e.future() and e.status in [cons.NEW, cons.ADQUIRED]))
    
    #
    # Episode Status Commands
    #
    def _mark(self, elist, status):
        print("Marking %d episode(s) as %s"%(len(elist), cons.ENUM_EPISODE_STATUS[status]["text"]))
        if len(elist): self.modified = True
        
        for e in elist:
            e.status = status
            print(e.print_str())
    
    def do_new(self, line):
        parser = ArgumentParser(prog="new", description="Mark episodes as NEW", epilog="example: new lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        l = episode.List()
        for pattern in args.filters:
            l.extend(self.episodes.filter(lambda e: e.match(pattern) and not e.future() and e.status in [cons.ADQUIRED, cons.SEEN]))
        
        self._mark(l, cons.NEW)
    
    def do_adquire(self, line):
        parser = ArgumentParser(prog="adquire", description="Mark episodes as ADQUIRED", epilog="example: adquire lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        l = episode.List()
        for pattern in args.filters:
            l.extend(self.episodes.filter(lambda e: e.match(pattern) and not e.future() and e.status in [cons.NEW]))
        
        self._mark(l, cons.ADQUIRED)
    
    def do_see(self, line):
        parser = ArgumentParser(prog="see", description="Mark episodes as SEEN", epilog="example: see lost.s01* lost.s02*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        l = episode.List()
        for pattern in args.filters:
            l.extend(self.episodes.filter(lambda e: e.match(pattern) and not e.future() and e.status in [cons.NEW, cons.ADQUIRED]))
        
        self._mark(l, cons.SEEN)
    
    #
    # Episode info Commands
    #
    def do_format(self, line):
        parser = ArgumentParser(prog="format", description="print episodes with given formats", epilog="example: format lost*")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        l = episode.List()
        for pattern in args.filters:
            l.extend(self.episodes.filter(lambda e: e.match(pattern) and not e.future() and e.status in [cons.NEW]))
        
        formats = self.main.get_formats()
        if len(formats) == 0:
            print("no formats defined, please check your config")
            return
        
        for e in l:
            for fmt in formats:
                print(e.format(fmt))
    
    def do_ls(self,line):
        parser = ArgumentParser(prog="ls", description="Show episodes information", epilog="example: ls -as lost*")
        parser.add_argument("-n", "--new", action="store_true", help="list NEW episodes (default)")
        parser.add_argument("-a", "--adquired", action="store_true", help="list ADQUIRED episodes (default)")
        parser.add_argument("-s", "--seen", action="store_true", help="list SEEN episodes")
        parser.add_argument("-f", "--future", action="store_true", help="list episodes not aired to date, implies -nas")
        parser.add_argument("filters", metavar="EPISODE", nargs="*", default=["*"], help="episode name or filter, ex: lost.s01e0*")
        
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        l = episode.List()
        for pattern in args.filters:
            l.extend(self.episodes.filter(lambda e: e.match(pattern)))
        
        # defaults: NEW and ADQUIRED
        if not (args.new or args.adquired or args.seen or args.future):
            args.new = args.adquired = True
        
        if args.future:
            l = l.filter(lambda e: e.future())
            # future implies every other status
            args.new = args.adquired = args.seen = True
        else:
            l = l.filter(lambda e: not e.future())
        
        if not args.new: l = l.filter(lambda e: e.status != cons.NEW)
        if not args.adquired: l = l.filter(lambda e: e.status != cons.ADQUIRED)
        if not args.seen: l = l.filter(lambda e: e.status != cons.SEEN)
        
        l.sort(key=lambda e: e.date, reverse = True)
        
        print(l.print_str())
    
    #
    # Auxiliary commands:
    #
    def do_version(self, line):
        print(__version__)
    
    def do_help(self, line):
        sep = "\n   "
        print("\nTo get specific help type: COMMAND --help\n")
        print("Auxiliary commands:"+sep+sep.join(["version", "exit", "quit", "help"]) + "\n")
        print("DB commands:"+sep+sep.join(["save", "reload"]) + "\n")
        print("Episodes commands:"+sep+sep.join(["update", "new", "adquire", "see", "format", "ls"]) + "\n")
        print("Shows commands:"+sep+sep.join(["shows", "search"]) + "\n")
    
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
        
        print("Invalid command: %s"%(line.split(" ")[0]))
        return self.do_help("")
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("^C")
            return self.cmdloop()
