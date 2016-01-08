__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import clips
from USS.DATA.Object import Object

class CLIPS(Object):
    def __init__(self, **argv):
        self.argv = argv
        self.clips = clips.Environment()
        self.clear()
        self.clips.PrintFacts()
    def clear(self):
        self.clips.Clear()
        self.clips.Reset()
    def current(self):
        self.clips.SetCurrent()
    def load(self, fname):
        self.clips.Load(fname)
    def facts(self, fname):
        self.clips.LoadFacts(fname)
    def return_facts(self, **argv):
        pass


if __name__ == '__main__':
    c = CLIPS()
    c.load("../../../etc/clips/ini/shared.clp")
    c.facts("../../../etc/cfg/shared.clp")
    c.clips.PrintFacts()
    print dir(c.clips)
    fl = c.clips.FactList()
    for f in fl:
        if  f.Relation == "shared_memory_segment":
            print f.Slots["key"], int(f.Slots["id"])
