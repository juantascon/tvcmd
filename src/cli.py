#! /usr/bin/env python2

import readline, cmd, sys
import episode, manager

class EpisodesCmd(cmd.Cmd, manager.Manager):

    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        self.load()
        
    def do_shows(self, line):
        print(self.db.list_shows())
    
    def _complete(self, text):
        return self.db.filter(status = episode.STATUS_NONE).complete_text(text)
    
    def do_see(self, line):
        eurls = self.db.filter_by_url_pattern(line)
        
        for eurl in eurls:
            eurl.update(status = episode.STATUS_SEEN)
            print(eurl.fmt_color())
    
    def complete_see(self, text, line, start_index, end_index):
        return self._complete(text)
    
    def do_ls(self, line):
        if not line:
            line = "*"
        
        for eurl in self.db.filter_by_url_pattern(line).filter(status=episode.STATUS_NONE):
            print(eurl.fmt_color())
    
    def complete_ls(self, text, line, start_index, end_index):
        return self._complete(text)
    
    def do_save(self, line):
        self.save()
    
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
