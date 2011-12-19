#! /usr/bin/env python2

import readline, cmd, sys
import config, manager

_manager = manager.Manager(config.SHOWS.data, config.SEEN.data)

class EpisodesCmd(cmd.Cmd):
    
    def do_see(self, line):
        l = _manager.see(line)
        for eurl in l:
            print(eurl.fmt_color(True))
            
    def complete_see(self, text, line, start_index, end_index):
        return _manager.complete(text)
    
    def do_ls(self, line):
        if not line:
            line = "*"
            
        for eurl in _manager.pending.filter(line):
            print(eurl.fmt_color(False))
    
    def complete_ls(self, text, line, start_index, end_index):
        return _manager.complete(text)
    
    def do_save(self, line):
        config.SEEN.data = _manager.seen.to_str_list()
        config.SEEN.save()

    ## Basic commands:
    def emptyline(self):
        pass
    
    def do_exit(self, arg):
        sys.exit(0)
        
    def do_quit(self, arg):
        self.do_exit(arg)
        
    def do_EOF(self, arg):
        print()
        self.do_exit(arg)
        
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print()
            self.do_exit("")
