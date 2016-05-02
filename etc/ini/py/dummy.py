__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

def main(*args, **argv):
    env = args[0]
    args = tuple(list(args[1:]))
    print "This startup function doesn't do much",env,repr(args),repr(argv)
