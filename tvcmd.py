#! /usr/bin/python

# this is only for python interactive mode


import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/lib/")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/src/")

import cli

tvcmd = cli.Cmd()

def interactive(argv):
    import readline
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    
    main(argv)
    
    import code
    code.interact(local=globals())

def main(argv):
    tvcmd.load()
    tvcmd.cmdloop()

if __name__ == "__main__":
    interactive(sys.argv)
