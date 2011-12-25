import inspect, sys, os

def version():
    return "DEV"

def msg(value):
    sys.stderr.write(value)
    sys.stderr.flush()

# def debug(value):
#     info = inspect.getframeinfo(inspect.stack()[1][0])
#     msg("DEBUG::%s.%s(): %s\n"%(os.path.basename(info.filename), info.function, value))
    
# def info(value):
#     msg("INFO::%s\n" %(value))

msg("Using tvcmd lib version: %s\n"%(version()))
