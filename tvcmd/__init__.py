import sys

__author__ = 'Juan Tascon'
__version__ = '0.9.1'
__license__ = 'GPL3'

def msg(value):
    sys.stderr.write(str(value))
    sys.stderr.flush()

msg("tvcmd version: %s\n"%(__version__))
