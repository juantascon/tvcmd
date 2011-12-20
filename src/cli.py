#! /usr/bin/env python2

import readline, cmd, sys
import episode, manager

class Cmd(cmd.Cmd, manager.Manager):

    def __init__(self):
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        self.load()
    
    def do_shows(self, line):
        print(self.db.list_shows())
        
    def complete_adquire(self, text, line, start_index, end_index):
        subdb = self.db.filter(status = episode.STATUS_NONE)
        return subdb.complete_text(text)
        
    def do_adquire(self, line):
        subdb = self.db.filter_by_url_pattern(line if line else "*")
        subdb = subdb.filter(status = episode.STATUS_NONE)
        
        for eurl in subdb:
            eurl.update(status = episode.STATUS_ADQUIRED)
            print(eurl.fmt_color())
            
    def complete_see(self, text, line, start_index, end_index):
        subdb = self.db.filter(status = episode.STATUS_NONE) + self.db.filter(status = episode.STATUS_ADQUIRED)
        return subdb.complete_text(text)
    
    def do_see(self, line):
        subdb = self.db.filter_by_url_pattern(line if line else "*")
        subdb = subdb.filter(status = episode.STATUS_NONE) + subdb.filter(status = episode.STATUS_ADQUIRED)
        
        for eurl in subdb:
            eurl.update(status = episode.STATUS_SEEN)
            print(eurl.fmt_color())
            
    def complete_ls(self, text, line, start_index, end_index):
        subdb = self.db.filter(status = episode.STATUS_NONE) + self.db.filter(status = episode.STATUS_ADQUIRED)
        return subdb.complete_text(text)
    
    def do_ls(self, line):
        subdb = self.db.filter_by_url_pattern(line if line else "*")
        subdb = subdb.filter(status = episode.STATUS_NONE) + subdb.filter(status = episode.STATUS_ADQUIRED)
        
        for eurl in subdb:
            print(eurl.fmt_color())
    
    def do_save(self, line):
        self.save()
    
    ## Basic commands:
    def emptyline(self):
        pass
    
    def do_exit(self, arg):
        sys.exit(0)
        
    def do_quit(se21lf, arg):
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
