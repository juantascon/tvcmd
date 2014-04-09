import readline, cmd, argparse
from . import manager, commands

from . import __version__

import logging
def log(): return logging.getLogger(__name__)

class CommandContainer():
    def __init__(self):
        self.reload = commands.Reload()
        self.update = commands.Update()
        self.save = commands.Save()
        self.shows = commands.Shows()
        self.search = commands.Search()
        self.new = commands.New()
        self.adquire = commands.Adquire()
        self.see = commands.See()
        self.format = commands.Format()
        self.ls = commands.Ls()

class Shell(cmd.Cmd):
    def __init__(self):
        readline.set_completer_delims(" ")
        super().__init__(self)
        
        self.prompt = "tvcmd:> "
        self.cmds = CommandContainer()
    
    
    #
    # bypass command handling to each command class
    #
    def do_reload(self, line):
        return self.cmds.reload.do(line)
    
    def do_update(self, line):
        return self.cmds.update.do(line)
    
    def do_save(self, line):
        return self.cmds.save.do(line)
    
    def do_shows(self, line):
        return self.cmds.shows.do(line)
    
    def do_search(self, line):
        return self.cmds.search.do(line)
    
    def do_format(self, line):
        return self.cmds.format.do(line)
        
    def complete_format(self, text, line, start_index, end_index):
        return self.cmds.format.complete(text, line, start_index, end_index)
                
    def do_adquire(self, line):
        return self.cmds.adquire.do(line)
        
    def complete_adquire(self, text, line, start_index, end_index):
        return self.cmds.adquire.complete(text, line, start_index, end_index)
    
    def do_new(self, line):
        return self.cmds.new.do(line)
        
    def complete_new(self, text, line, start_index, end_index):
        return self.cmds.new.complete(text, line, start_index, end_index)
    
    def do_see(self, line):
        return self.cmds.see.do(line)
        
    def complete_see(self, text, line, start_index, end_index):
        return self.cmds.see.complete(text, line, start_index, end_index)
        
    def do_ls(self,line):
        return self.cmds.ls.do(line)
        
    def complete_ls(self, text, line, start_index, end_index):
        return self.cmds.ls.complete(text, line, start_index, end_index)
    
    
    #
    # basic commands
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
    
    def emptyline(self):
        pass
    
    #TODO:
    #def do_exit(self, line):
    #    if self.modified:
    #        answer = self.ask_yn("Database has been modified. Do you want to save it now?")
    #        if answer: return self.save()
    #    return True
        
    #do_quit = do_exit
    
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
