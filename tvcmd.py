#! /usr/bin/env python

import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/lib/")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))+"/src/")

def main(argv):
    import cli
    cli.EpisodesCmd().cmdloop()
    
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))






