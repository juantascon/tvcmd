import inspect, sys, os

def version(): return "0.8.3"

def msg(value):
    sys.stderr.write(str(value))
    sys.stderr.flush()

# def debug(value):
#     info = inspect.getframeinfo(inspect.stack()[1][0])
#     msg("DEBUG::%s.%s(): %s\n"%(os.path.basename(info.filename), info.function, value))
    
# def info(value):
#     msg("INFO::%s\n" %(value))

msg("tvcmd version: %s\n"%(version()))
