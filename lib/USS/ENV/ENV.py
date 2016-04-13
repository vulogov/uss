__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import sys
from PYCLP import PYCLP

class ENV(PYCLP):
    def __init__(self, **argv):
        apply(PYCLP.__init__, (self,), argv)
        self.Object__set_attr("argv", self.argv)


def main(*args):
    if not args and not sys.argv:
        return None
    elif args:
        path = args[0]
    elif sys.argv:
        path = sys.argv[0]
    env = ENV(path=path)
    try:
        env.load(file="%s/bootstrap.clp"%path)
        env.facts("%s/configuration.clp"%path)
    except KeyboardInterrupt:
        return None
    return env