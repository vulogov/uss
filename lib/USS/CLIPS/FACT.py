__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

class FACT:
    def facts(self, fname):
        self.clips.LoadFacts(fname)
    def load_facts(self, **args):
        return self._load(self.clips.LoadFacts, self.clips.LoadFactsFromString, args)

