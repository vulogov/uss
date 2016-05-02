__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import sys
from PYCLP import PYCLP

class ENV(PYCLP):
    def __init__(self, **argv):
        apply(PYCLP.__init__, (self,), argv)
        self.Object__set_attr("argv", self.argv)
    def filter(self, **args):
        out = []
        for f in self.clips.FactList():
            if args.has_key("relation") and f.Relation == args["relation"]:
                out.append(f)
                continue
            for k in args.keys():
                if k == "relation":
                    continue
                if f.Slots.has_key(k) and f.Slots[k] == args[k]:
                    out.append(f)
        return out



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
        env.clips.Run()
        for m in  env.filter(relation="py_module"):
            env += m.Slots["path"]
        env.reload_mods()
        for m in env.filter(relation="start"):
            env(m.Slots["name"], env)
    except KeyboardInterrupt:
        return None
    return env