__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import clips
from USS.DATA.Object import Object
from LOADER import LOADER
from FACT import FACT
from CLPEXEC import CLPEXEC

class CLP(Object, LOADER, FACT, CLPEXEC):
    def __init__(self, **argv):
        self.argv = argv
        self.clips = clips.Environment()
        self.clear()
    def clear(self):
        self.clips.Clear()
        self.clips.Reset()
    def current(self):
        self.clips.SetCurrent()



if __name__ == '__main__':
    c = CLP()
    c.load(file="../../../etc/bootstrap.clp")
    print 1
    c.facts("/root/SRC/uss/etc/configuration.clp")
    c.clips.PrintFacts()
    print dir(c.clips)
    fl = c.clips.FactList()
    for f in fl:
        if  f.Relation == "shared_memory_segment":
            print f.Slots["key"], int(f.Slots["id"])
