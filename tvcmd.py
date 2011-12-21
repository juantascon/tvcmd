#! /usr/bin/python

import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/lib/")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/src/")

import cli

tvcmd = cli.Cmd()

def interactive():
    import readline
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    
    import code
    code.interact(local=globals())

def main(argv):
    tvcmd.load()
    
    # print torrent urls and exit
    if "-t" in argv:
        tvcmd.onecmd("tor *")
    # main execution mode
    else:
        tvcmd.cmdloop()
        interactive()
        
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    main(sys.argv)
    
