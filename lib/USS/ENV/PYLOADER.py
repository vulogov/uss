__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import imp
from FS import *

class PYLOADER:
    def __init__(self):
        self.mods = {}
    def find_the_mod(self, mod_name):
        for p in self.mods.keys():
            if self.mods[p].has_key(mod_name):
                return self.mods[p][mod_name]
        return None
    def reload_mods(self):
        for p in self.path:
            if not self.mods.has_key(p):
                self.mods[p] = {}
            dir = get_dir_content(p)
            for m in dir:
                file, full_path, mod = m
                modname, ext = mod
                if ext not in [".py",] or self.find_the_mod(modname) != None:
                    continue
                try:
                    _mod = imp.load_source(modname, full_path)
                except KeyboardInterrupt:
                    continue
                self.mods[p][modname] = _mod
        for p in self.mods.keys():
            if p not in self.path:
                del self.mods[p]
