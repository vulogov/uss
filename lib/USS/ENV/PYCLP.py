__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import clips
from PY import PY
from USS.CLIPS.CLP import CLP

class PYCLP(PY,CLP):
    def __init__(self, **argv):
        self.argv = argv
        self.path = []
        self.Object__set_attr("path", self.argv)
        apply(PY.__init__, tuple([self,] + [self.path,]))
        apply(CLP.__init__, (self,), argv)
    def load_pyclp_module(self, name):
        import fnmatch
        from USS.DATA.MISC.STR import rchop
        mod = self.find_the_mod(name)
        if mod == None:
            raise ValueError, "PYCLP moduylr %s not found"%name
        c = 0
        for e in dir(mod):
            if fnmatch.fnmatch(e, "*_clips"):
                fun_name = rchop(e,"_clips")
                try:
                    fun = getattr(mod, fun_name)
                except:
                    continue
                clips.RegisterPythonFunction(fun)
                print getattr(mod, e)
                self.clips.Build(getattr(mod, e))
                c += 1
        return c

if __name__ == '__main__':
    pc = PYCLP(path=["../../../etc/bind",])
    pc.load_pyclp_module("match")
    print pc.clips.Eval('(filename_match "test.txt" "*.txt")')
    exp = '(re_match "vfs.fs.size[/,pfree]" "vfs.fs.size\\\\[(.?),pfree\\\\]")'
    print repr(exp)
    print pc.clips.Eval(exp)




