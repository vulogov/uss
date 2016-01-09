__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class CLPEXEC:
    def load(self, **args):
        return self._load(self.clips.Load, self.clips.Eval, args)
    def execute(self, **args):
        return self._load(self.clips.BatchStar, self.clips.Eval, args)

