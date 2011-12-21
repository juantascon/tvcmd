#! /usr/bin/python

import sys, os

import tvcmd.cli

ui = tvcmd.cli.Cmd()

def interactive():
    import readline
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    
    import code
    code.interact(local=globals())
    
def main(argv):
    ui.load()
    
    # print torrent urls and exit
    if "-t" in argv:
        ui.onecmd("tor *")
    # main execution mode
    else:
        ui.cmdloop()
        interactive()
        
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    main(sys.argv)
    
